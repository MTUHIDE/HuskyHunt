from catalog.models import CatalogItem, Category
from accountant.models import user_profile
from profanity_check.models import ArchivedType
from .moderationEmails import *
import math
from datetime import datetime, timedelta
import pytz

# Ignores a report
# Sets reported=False
def ignore_report(queryset):
    queryset.update(reported=False)

# Removes an item
# Sets reported=True, archived=True, type=Removed
def remove_item(queryset, reason):
    queryset.update(reported=True)
    queryset.update(archived=True)
    queryset.update(archivedType=ArchivedType.Types.REMOVED)
    # Decrement number of points by three
    for item in queryset:
        profile = user_profile.objects.get(user = item.username)
        profile.points = profile.points - 3
        profile.save()

        autoSuspensionDuration = __getSuspensionDuration(profile);
        __suspend_user_helper(user_profile.objects.filter(user = item.username), autoSuspensionDuration);

        sendRemoveItemEmail(item, reason, autoSuspensionDuration)

# Makes an item public
# Sets reported=false, archived=False, type=Visible
def make_item_public(queryset):
    queryset.update(reported=False)
    queryset.update(archived=False)
    queryset.update(archivedType=ArchivedType.Types.VISIBLE)

    for item in queryset:
        sendApproveItemEmail(item)

# Removes a ride
# Sets reported=True, archived=True, type=Removed
def remove_ride(queryset, reason):
    queryset.update(reported=True)
    queryset.update(archived=True)
    queryset.update(archivedType=ArchivedType.Types.REMOVED)
    # Decrement number of points by three
    for ride in queryset:
        profile = user_profile.objects.get(user = ride.username)
        profile.points = profile.points - 3
        profile.save

        autoSuspensionDuration = __getSuspensionDuration(profile);
        __suspend_user_helper(user_profile.objects.filter(user = ride.username), autoSuspensionDuration);

        sendRemoveRideEmail(ride, reason, autoSuspensionDuration)

# Makes a ride public
# Sets reported=false, archived=False, type=Visible
def make_ride_public(queryset):
    queryset.update(reported=False)
    queryset.update(archived=False)
    queryset.update(archivedType=ArchivedType.Types.VISIBLE)

    for ride in queryset:
        sendApproveRideEmail(ride)

# Suspends a user for a specifed duration
# Parameters:
#   queryset: Queryset of user_profiles to suspend
#   reason: The reason for the suspension (string)
#   duration: Duration of the suspension in days
#       greater than 31 days is a ban.
def suspend_user(queryset, reason, duration):
    suspensionString = __suspend_user_helper(queryset, duration)

    for user in queryset:
        if suspensionString != '':
            if isinstance(user, user_profile):
                sendSuspendUserEmail(user.user, suspensionString, reason)
            else:
                sendSuspendUserEmail(user, suspensionString, reason)

# Helper function to suspend users without sending an email
def __suspend_user_helper(queryset, duration):
    suspensionDuration = 0;
    suspensionString = '';

    if duration <= 0:
        suspensionString = '';
    elif duration <= 7:
        suspensionDuration = 7
        suspensionString = 'seven'
    elif duration <= 31:
        suspensionDuration = 30
        sespensionString = 'thirty'
    else:
        suspensionDuration = 1000
        suspensionString = 'banned'

    # Timeout users
    if suspensionDuration > 0:
        banned_untilDateTime = (datetime.now() + timedelta(days=suspensionDuration)).astimezone(pytz.timezone('UTC'))
        queryset.update(banned_until = banned_untilDateTime)

    return suspensionString

# Determines if a suspension should be given
# And if so, executes that suspension
# Returns the duration of the suspension in days
def __getSuspensionDuration(profile):
    if (profile.points < -20):
    	return math.inf
    elif (profile.points < -10):
    	return 30
    elif (profile.points < -5): 
    	return 7
    else:
    	return 0
