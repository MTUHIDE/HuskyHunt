from django_cron import CronJobBase, Schedule
from rideSharing.models import RideItem
from datetime import date
from django.utils import timezone
from profanity_check import ArchivedType


# Used to archive rides that have already "left"
class ArchiveRides(CronJobBase):
    RUN_AT_TIMES = ['04:00'] # Run at 4am

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'rideSharing.archive_rides'    # a unique code

    def do(self):
        today = date.today()

        # Considered archived after the ride has left
        archive_rides = RideItem.objects.filter(
            archived=ArchivedType.Q_myContent,
            date_leaving__lte=today
        )

        # For each ride, set it to archived
        for ride in old_rides:
        	ride.archived = "True"
        	ride.save()

# Used to delete old archived rides
class deleteOldRides(CronJobBase):
    RUN_AT_TIMES = ['04:00'] # Run at 4am

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'catalog.deleteOldRides'    # a unique code

    def do(self):
        today = timezone.now()
        delete_time = today - timezone.timedelta(weeks=16) # Considered to be deleted if the ride left more than 16 weeks ago

        # Get the rides that left before today
        delete_rides = RideItem.objects.filter(
            archived='True',
            date_leaving__lte=delete_time
        )

        # Delete these old rides
        delete_rides.delete()
