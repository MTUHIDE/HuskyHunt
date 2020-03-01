from django_cron import CronJobBase, Schedule
from rideSharing.models import RideItem
from datetime import date


# Used to archive rides that have already "left"
class ArchiveRides(CronJobBase):
    RUN_AT_TIMES = ['04:00'] # Run at 4am

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'rideSharing.archive_rides'    # a unique code

    def do(self):
        today = date.today()

        # Get the rides that left before today
        old_rides = RideItem.objects.filter(
            archived='False',
            date_leaving__lte=today
        )

        # For each ride, set it to archived
        for ride in old_rides:
        	ride.archived = "True"
        	ride.save()