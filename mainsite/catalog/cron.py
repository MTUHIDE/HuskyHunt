from django_cron import CronJobBase, Schedule
from catalog.models import CatalogItem
from datetime import date, timedelta
from django.utils import timezone
from profanity_check.models import ArchivedType
from accountant.models import user_profile
from django.core.mail import get_connection

# HTML EMAIL
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None,
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.
    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


# Sends a weekly email with new posts for the week
class digestEmail(CronJobBase):
    RUN_EVERY_MINS = 10080  # Run every 7 days

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'catalog.digestEmail'  # a unique code

    def do(self):
        today = timezone.now()
        lastWeek = today - timezone.timedelta(weeks=1)  # Considered latest items in last week

        # Get public items in last week
        latestItems = CatalogItem.objects.filter(
            archived='False',
            archivedType='VI',
            date_added__gte=lastWeek
        )

        if latestItems.count() == 0:
            return "No new items to include in weekly email!"

        users = user_profile.objects.filter(digest=True)
        allMessages = list(())

        for user in users:
            html_content = render_to_string("digest_template.html", {'user': user, 'items': latestItems})
            text_content = strip_tags(html_content)
            email = (
                'HuskyHunt Weekly Digest',  # subject
                text_content,  # text content
                html_content,  # html content
                'Admin via HuskyHunt <admin@huskyhunt.com>',  # from email
                [user.user.email]  # to email
            )
            allMessages.append(email)

        successfullySent = send_mass_html_mail(tuple(allMessages), fail_silently=False)

        message = "Successfully sent " + str(successfullySent) + " emails out of " + str(len(allMessages))
        return message


# Used to archive items that are old
class archiveOldItems(CronJobBase):
    RUN_AT_TIMES = ['04:00']  # Run at 4am

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'catalog.archiveOldItems'  # a unique code

    def do(self):
        today = timezone.now()
        archive_time = today - timezone.timedelta(weeks=6)  # Considered to be archived 6 weeks before today

        # Get the items that left before today
        archive_items = CatalogItem.objects.filter(
            archived='False',
            archivedType='VI',
            date_added__lte=archive_time
        )

        message = "Archived the following items: "

        # For each item, set it to archived
        for item in archive_items:
            item.archived = 'True'
            item.archivedType = ArchivedType.Types.ARCHIVED
            item.save()
            message += "'" + item.item_title + "', "

        return message


# Used to delete old archived items
class deleteOldItems(CronJobBase):
    RUN_AT_TIMES = ['04:00']  # Run at 4am

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'catalog.deleteOldItems'  # a unique code

    def do(self):
        today = timezone.now()
        delete_time = today - timezone.timedelta(weeks=16)  # Considered to be deleted 16 weeks before today

        # Get the items that left before today
        delete_items = CatalogItem.objects.filter(
            archived='True',
            date_added__lte=delete_time
        )

        message = "Deleted the following items: "

        # For each item, set it to archived
        for item in delete_items:
            message += "'" + item.item_title + "', "

        # Delete these old items
        delete_items.delete()

        return message
