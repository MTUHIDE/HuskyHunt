from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from catalog.views import isUserNotBanned
from catalog.models import CatalogItem
from accountant.models import user_profile
from profanity_check.models import ArchivedType

# Create your views here.

# This helper function checks if a user is a moderator
def isUserModerator(username):
    return username.is_staff           # The user is staff

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

    reported_items = CatalogItem.objects.filter(
        archived='True', reported='True', archivedType=ArchivedType.Types.HIDDEN
    ).order_by('-date_added')[:500]
    
    reported_items_pictures = {}

    first = reported_items.first()

    #Packages the information to be displayed into context
    context = {
        'title': title,
        'reported_items': reported_items,
        'reported_items_pictures': reported_items_pictures,
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
        item = CatalogItem.objects.get(pk=pk)
    except CatalogItem.DoesNotExist:
        return HttpResponseRedirect(reverse('moderation:index'))

    item.reported = False
    item.archived = False
    item.archivedType=ArchivedType.Types.VISIBLE


    item.save()

    context = {
        'title': title,
    }

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
