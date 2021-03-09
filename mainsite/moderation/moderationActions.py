from catalog.models import CatalogItem, Category
from accountant.models import user_profile
from profanity_check.models import ArchivedType
from .moderationEmails import *
import math

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

        sendRemoveItemEmail(item, reason, should_issue_suspension(profile))

# Allows an item
# reported=False, archived=False, type=visble
def allow_item(queryset):
    queryset.update(reported=False)
    queryset.update(archived=False)
    queryset.update(archivedType=ArchivedType.Types.VISIBLE)

#def ignore_item_report(queryset):


# Determines if a suspension should be given
# And if so, executes that suspension
# Returns the duration of the suspension in days
def should_issue_suspension(profile):
    if (profile.points < 20):
    	return math.inf
    elif (profile.points < 10):
    	return 30
    elif (profile.points < 5): 
    	return 7
    else:
    	return 0
