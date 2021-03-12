from catalog.models import CatalogItem, Category
from accountant.models import user_profile
from profanity_check.models import ArchivedType
from .moderationEmails import *
import math

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

        sendRemoveItemEmail(item, reason, getSuspensionDuration(profile))

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
        profile.save()

        sendRemoveRideEmail(ride, reason, getSuspensionDuration(profile))

# Makes a ride public
# Sets reported=false, archived=False, type=Visible
def make_ride_public(queryset):
    queryset.update(reported=False)
    queryset.update(archived=False)
    queryset.update(archivedType=ArchivedType.Types.VISIBLE)

    for ride in queryset:
        sendApproveRideEmail(ride)

# ------------------------------------------------------
# TODO
# - User suspension & ban functionality
# - Make admin functions use our moderation actions here
# ------------------------------------------------------

# Determines if a suspension should be given
# And if so, executes that suspension
# Returns the duration of the suspension in days
def getSuspensionDuration(profile):
    if (profile.points < 20):
    	return math.inf
    elif (profile.points < 10):
    	return 30
    elif (profile.points < 5): 
    	return 7
    else:
    	return 0
