from django_cron import CronJobBase, Schedule
from catalog.models import CatalogItem
from datetime import date, timedelta
from django.utils import timezone
from profanity_check.models import ArchivedType

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
