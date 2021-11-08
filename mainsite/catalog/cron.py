from django_cron import CronJobBase, Schedule
from catalog.models import CatalogItem
from datetime import date, timedelta
from django.utils import timezone
from profanity_check.models import ArchivedType
from accountant.models import user_profile
from django.core.mail import BadHeaderError, EmailMessage, send_mass_mail

# Sends a weekly email with new posts for the week
class digestEmail(CronJobBase):
    RUN_EVERY_MINS = 10080; # Run every 7 days

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'catalog.digestEmail'    # a unique code

    def do(self):
        today = timezone.now()
        lastWeek = today - timezone.timedelta(weeks=1)  # Considered latest items in last week

        # Get public items in last week
        latestItems = CatalogItem.objects.filter(
            archived='False',
            archivedType='VI',
            date_added__gte=lastWeek
        )

        message = "Found the following most recent items: "

        # For each item found, copy it to the message
        for item in latestItems:
            message += "'" + item.item_title + "', "

        users = user_profile.objects.filter(digest = True);
        allMessages = list(());

        for user in users:
            emailBody = (
                'hello ' + user.user.first_name + ',\n\n' +
                'We thought you would like to know about recent items you might have missed!\n'
            );

            for item in latestItems:
                emailBody += item.item_title + '\n'

            email = (
                'HuskyHunt Weekly Digest', # subject
                emailBody, #body
                'Admin via HuskyHunt <admin@huskyhunt.com>', # from_email
                [user.user.email]  # to email
                )
            
            allMessages.append(email)

        message1 = ('Subject here', 'Here is the message', 'Admin via HuskyHunt <admin@huskyhunt.com>', ['cjvidro@mtu.edu'])
        successfullySent = send_mass_mail(tuple(allMessages), fail_silently=False)

        message += "\n\n Successfully sent " + str(successfullySent) + " emails out of " + str(len(allMessages));
        return message;
            

# Used to archive items that are old
class archiveOldItems(CronJobBase):
    RUN_AT_TIMES = ['04:00'] # Run at 4am

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'catalog.archiveOldItems'    # a unique code

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

        return message;

# Used to delete old archived items
class deleteOldItems(CronJobBase):
    RUN_AT_TIMES = ['04:00'] # Run at 4am

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'catalog.deleteOldItems'    # a unique code

    def do(self):
        today = timezone.now()
        delete_time = today - timezone.timedelta(weeks=16) # Considered to be deleted 16 weeks before today

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
