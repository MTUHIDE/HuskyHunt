from django_cron import CronJobBase, Schedule
from rideSharing.models import RideItem


# Used to archive rides that have already "left"
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'rideSharing.my_cron_job'    # a unique code

    def do(self):
        pass    # do your thing here