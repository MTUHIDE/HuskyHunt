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
        archive_time = today - timezone.timedelta(weeks=4)  # Considered to be archived 4 weeks before today

        # Get the items that left before today
        archive_items = CatalogItem.objects.filter(
            archived=ArchivedType.Q_myContent,
            date_added__lte=archive_time
        )

        # For each item, set it to archived
        for item in archive_items:
            item.archived = "True"
            item.archivedType = ArchivedType.Types.ARCHIVED
            item.save()

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

        # Delete these old items
        delete_items.delete()
