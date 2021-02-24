from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from catalog.views import isUserNotBanned
from catalog.models import CatalogItem
from accountant.models import user_profile
from accountant.admin import archiveAllUserPosts
from profanity_check.models import ArchivedType
from rideSharing.models import RideItem
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from datetime import datetime, timedelta
import pytz
import math
# Create your views here.


# This helper function checks if a user is a moderator
def isUserModerator(username):
    return username.is_staff           # The user is staff

# Allows us to paginate different models.
def getPage(queries, limit_per_page, current_page_number):

    # Get the total items in the query
    total_items = 0

    for query in queries:
        total_items += query.count()

    # Get the total pages
    total_pages = math.ceil(total_items / limit_per_page)

    # Check the current page number
    current_page_number = max(0, min(current_page_number, total_pages))

    # Create the results variable.
    query_results = {}

    # fill the page
    i = 0
    results_found = 0
    start_index = (current_page_number - 1) * limit_per_page
    end_index = (current_page_number * limit_per_page) - 1
    for query in queries:
        # We have already scanned all we need at this point.
        if end_index < 0:
            query_results[i] = []
            i += 1
            continue
        
        # Get the items from the query.
        count = query.count()

        # Check the start index
        if start_index > 0:
            start_index -= count
            if start_index < 0:
                start_index = 0

        # Only get results if they're in range.
        if not start_index > count:
            query_results[i] = query[start_index:end_index]
        else:
            query_results[i] = []

        # Decriment the end index.
        end_index -= count

        # Increment i
        i += 1

    # Create the page variable
    page = {
        'total_pages': total_pages,
        'current_page': current_page_number,
        'next_page': min(current_page_number + 1, total_pages),
        'previous_page': max(1, current_page_number - 1),
        'results': query_results
    }

    return page

#This small helper function adds an appropriate congradulation message to the page
#param: context - the context that's normally passed to the catalog pages;
#         it's modified appropriately during this function to contain recent items
#param: type - one of 'SearchFail', 'FilterFail', 'PageNotFoundFail', etc.
#param: num_items - The number of recent items displayed, default is 4 most recent
#returns: boolean whether or not
def addCongratsOnEmpty(context, type, num_items = 4):
    context['failed_search'] = None
    if context['items'].paginator.count == 0:

        #Gets num_items most recent items from the database and sorts by date added
        recent_items = CatalogItem.objects.filter(
            archived='False',
            date_added__lte=timezone.now()
        ).order_by('-date_added')[:num_items]

        # Paginator will show up to num_items items. Always one page long.
        paginator = Paginator(recent_items, num_items, allow_empty_first_page=True)
        items = paginator.get_page(1)


        context['failed_search'] = type
        context['items'] = items
        return True
    return False

#This function gets all the items from the database
#and displays them to the screen sorted by most recently added
#param: request - array variable that is passed around the website, kinda like global variables
#returns: all the items in the database, with the most recently item added at the top
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
@user_passes_test(isUserModerator, login_url='/', redirect_field_name='/')
def index(request):
    

    #The CSS for this function can be found here
    template = 'moderation/index.html'
    #The title for the webpage
    title = "MTU Moderation"

    # Query for reported items.
    reported_items = CatalogItem.objects.filter(
        archived='True', reported='True', archivedType=ArchivedType.Types.HIDDEN
    ).order_by('-date_added')

    # Query for reported rides.
    reported_rides = RideItem.objects.filter(
        archived='True', reported='True', archivedType=ArchivedType.Types.REMOVED
    ).order_by('-date_added')

    #TODO: Remove this
    a_item = reported_items.first()
    a_ride = reported_rides.first()

    # Get the page number from the request. Default to 1.
    page_number = request.GET.get('page_number')
    if page_number is None:
        page_number = 1

    # Get the page from our function.
    page = getPage([reported_items, reported_rides], 10, page_number)

    


    # Set our variables.
    reported_items = page['results'][0]
    reported_rides = page['results'][1]
    reported_ids = set()

    # Find all reported ids.
    for item in reported_items:
        reported_ids.add(item.username_id)

    for ride in reported_rides:
        reported_ids.add(ride.username_id)

    # Get all reported profiles.
    reported_profile_list = list(user_profile.objects.filter(pk__in=reported_ids))

    reported_ids = None

    reported_profiles = {}

    for profile in reported_profile_list:
        reported_profiles[profile.id] = profile

    reported_profile_list = None

    #a_profile = reported_profiles.first()

    my_filter = request.GET.get('filter')

    #if my_filter == "Ridesharing":

    #elif my_filter == "Item Catalog":

    #else:


    #for a_profile in reported_profiles:
    #    print("h")

    #filters = ["Ridesharing", ]

    #Packages the information to be displayed into context
    context = {
        'title': title,
        'reported_items': reported_items,
        'reported_rides': reported_rides,
        'reported_profiles': reported_profiles,
    }

    #Displays all the items from the database with repect to the CSS template
    return render(request, template, context)

@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
@user_passes_test(isUserModerator, login_url='/', redirect_field_name='/')
def approve(request, pk):
    template = 'moderation/index.html'
    title = 'MTU Moderation'

    try:
        user = CatalogItem.objects.get(pk=pk)
    except CatalogItem.DoesNotExist:
        return HttpResponseRedirect(reverse('moderation:index'))

    ban_user(queryset=user)

    return index(request)

@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
@user_passes_test(isUserModerator, login_url='/', redirect_field_name='/')
def deny(request, pk):
    template = 'moderation/index.html'
    title = 'MTU Moderation'

    try:
        item = CatalogItem.objects.get(pk=pk)
    except CatalogItem.DoesNotExist:
        return HttpResponseRedirect(reverse('moderation:index'))

    item.reported = True
    item.archived = True
    item.archivedType=ArchivedType.Types.REMOVED

    profile = user_profile.objects.get(user = item.username)
    profile.points = profile.points - 3
    profile.save()

    item.save()

    context = {
        'title': title,
    }

    return index(request)

@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
@user_passes_test(isUserModerator, login_url='/', redirect_field_name='/')
def ban(request, pk):
    template = 'moderation/index.html'
    title = 'MTU Moderation'

    try:
        users = user_profile.objects.filter(pk=pk)
    except CatalogItem.DoesNotExist:
        return HttpResponseRedirect(reverse('moderation:index'))

    # Reset points, ban user(s) for 1000 days
    users.update(points=0)
    banned_untilDateTime = (datetime.now() + timedelta(days=1000)).astimezone(pytz.timezone('UTC'))
    users.update(banned_until = banned_untilDateTime)

    # Send emails
    for user in users:
        archiveAllUserPosts(user)

        #The body of the email
        message = ('Your account on HuskyHunt has been banned.\n'
            + 'For more information, contact the HuskyHunt team at huskyhunt-l@mtu.edu\n\nThis is an automated message.')

        #The email that this message is sent from
        from_email = 'Admin via HuskyHunt <admin@huskyhunt.com>'
        to_email = user.user.email

        email = EmailMessage(
            'Account Banned', # subject
            message, #body
            from_email, # from_email
            [to_email],  # to email
            reply_to=['huskyhunt-l@mtu.edu'],  # reply to email
            )
        email.send();

    context = {
        'title': title,
    }

    return index(request)