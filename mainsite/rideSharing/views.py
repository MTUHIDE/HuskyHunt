import re   #eeeeee

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.contrib import auth
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages
from rideSharing.models import RideItem, RideCategory
from django import forms
from django.core.paginator import Paginator

#This small helper function adds an appropriate error message to the page
#param: context - the context that's normally passed to the catalog pages;
#         it's modified appropriately during this function to contain recent items
#param: type - one of 'SearchFail', 'FilterFail', 'PageNotFoundFail', etc.
#param: num_items - The number of recent items displayed, default is 4 most recent
#returns: boolean whether or not
def addErrorOnEmpty(context, type, num_items = 4):
    context['failed_search'] = None
    if context['rides'].paginator.count == 0:

        #Gets num_items most recent items from the database and sorts by date added
        recent_rides = RideItem.objects.filter(
            archived='False',
            date_added__lte=timezone.now()
        ).order_by('-date_added')[:num_items]

        # Paginator will show up to num_items items. Always one page long.
        paginator = Paginator(recent_rides, num_items, allow_empty_first_page=True)
        rides = paginator.get_page(1)

        context['failed_search'] = type
        context['rides'] = rides
        return True
    return False

#This function sends a prepared email message to a seller
#param: request - array variable that is passed around the website, kinda like global variables
#param: pk - a int variable that is used as the primary key for the item in the database
#returns: The same page that the user is currently on
def email(request, pk):
    #Checks if the user has logged in
    if request.user.is_authenticated:

        #The subject line of the email
        subject = "Interested in your ride"

        #The body of the email
        message = (request.user.get_short_name() +
                  ' has messaged you about a ride you posted on HuskyHunt!\n\n' +
                  'Message from ' + request.user.get_short_name() + ': ' + request.GET['message'] +
                  '\n\nYou can respond by replying to this email, or by contacting ' + 
                  request.user.get_short_name() + ' directly: ' + request.user.email)

        #The email that this message is sent from
        from_email = request.user.get_short_name() + ' via HuskyHunt <' + request.user.email + '>'
        #Gets the item that is currently being viewed
        ride_item = RideItem.objects.filter(pk=pk)
        #Creates a variable to later store the sellers email
        to_email = ''

        #need to add an email to ride item. for now assume username is mtu username

        #For each loop that iterates on the number of items being currently viewed? Need to ask isaac about this
        for ride in ride_item:
            #Sets the recipient of the email as the sellers email from the database
            to_email = ride.username.email

        #Checks if the message is no empty
        if (request.GET['message'] != ''):

            #Sends the email with a subject, body, the sender, and the recipient
            send_mail(subject, message, from_email, [to_email], fail_silently=False,)
            #Displays that the email was sent successfully
            messages.error(request, 'Message sent successfully!')

        #If the message is empty then an error message is displayed
        else:
            messages.error(request, 'Please enter a message!')

        #Redirects the user to the same webpage (So nothing changes but the success message appearing)
        return HttpResponseRedirect('/ridesharing/' + str(pk))

    #If not logged in then the user is sent to the Husky Statue
    else:
        return HttpResponseRedirect('/')

#This function gets all the items from the database
#and displays them to the screen sorted by most recently added
#param: request - array variable that is passed around the website, kinda like global variables
#returns: all the items in the database, with the most recently item added at the top
def index(request):

    #The CSS for this function can be found here
    template = 'rideSharing/index.html'
    #The title for the webpage
    title = "MTU Ridesharing"

    failed_search = None
    if request.session.has_key('index_redirect_failed_search') and request.session['index_redirect_failed_search'] is not None:
        failed_search = request.session['index_redirect_failed_search']
        request.session['index_redirect_failed_search'] = None

    #Checks if the user is logged in
    if request.user.is_authenticated:

        #Gets 500 most recent items from the database and sorts by date added
        recent_items = RideItem.objects.filter(
            archived='False',
            date_added__lte=timezone.now()
        ).order_by('-date_added')[:500]

        #The filters dropdown containing all the categories (need to get a default category)
        filters = RideCategory.objects.all()

        # Paginator will show 16 items per page
        paginator = Paginator(recent_items, 16, allow_empty_first_page=True)
        page = request.GET.get('page') # Gets the page number to display
        rides = paginator.get_page(page)


        #Packages the information to be displayed into context
        context = {
            'title': title,
            'rides': rides,
            'search': 0,
            'filters': filters,
            'failed_search': failed_search
        }

        #Displays all the items from the database with repect to the CSS template
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')


#This small helper function adds an appropriate error message to the page
#param: context - the context that's normally passed to the ridesharing pages;
#         it's modified appropriately during this function to contain recent rides
#param: type - one of 'SearchFail', 'FilterFail', 'PageNotFoundFail', etc.
#param: num_items - The number of recent rides displayed, default is 4 most recent
#returns: boolean whether or not
def addErrorOnEmpty(context, type, num_items = 4):
    context['failed_search'] = None
    if context['rides'].paginator.count == 0:

        #Gets num_items most recent items from the database and sorts by date added
        recent_items = RideItem.objects.filter(
            archived='False',
            date_added__lte=timezone.now()
        ).order_by('-date_added')[:num_items]

        # Paginator will show up to num_items items. Always one page long.
        paginator = Paginator(recent_items, num_items, allow_empty_first_page=True)
        rides = paginator.get_page(1)


        context['failed_search'] = type
        context['rides'] = rides
        return True
    return False

#This function takes information from the search textfield
#param: request - array variable that is passed around the website, kinda like global variables
#returns: all items in the database that contain the string
#from the search text field in their name or description
def search(request):
    #The CSS code for this function can be found here
    template = 'rideSharing/index.html'

    #The title for the webpage
    title = 'MTU Ridesharing'

    #Checks to make sure the user has logged in
    if request.user.is_authenticated:
        #Uses the filter function to get the data of the searched items
        recent_items = RideItem.objects.filter(
            Q(start_city__contains=request.GET['search']) |
            Q(start_state__contains=request.GET['search']) |
            Q(start_zipcode__contains=request.GET['search']) |
            Q(destination_city__contains=request.GET['search']) |
            Q(destination_state__contains=request.GET['search']) |
            Q(destination_zipcode__contains=request.GET['search']) |
            Q(notes__contains=request.GET['search']),
            archived='False'
        )

        search_split = []
        radius = 69.0 # There are genuinely approximately 69 miles to a degree latitude
        crResults = re.match(r'\[\s*(?P<a>\-?\d{1,3}(?:\.\d+)?)\s*\,\s*(?P<b>\-?\d{1,3}(?:\.\d+)?)\s*(?:\,\s*(?P<c>\d+(?:\.\d+)?)\s*)?(?:\,\s*(?P<d>[^\]]+)\s*)?\]', request.GET['search'])
        if(crResults is not None):
            lat = float(crResults.group('a'))
            lon = float(crResults.group('b'))
            if(crResults.group('c') is not None):
                radius = float(crResults.group('c'))
            dres = crResults.group('d')
            dres = dres if dres else 0
            search_split.append(["coor", [lat, lon, radius], dres])

            # Note: this search region isn't a circle,
            # it isn't even a square. It's a weird oblong trapezoid that gets less accurate as you get further north
            close_items = RideItem.objects\
            .filter(destination_coordinates_lat__lte=lat + radius / 69)\
            .filter(destination_coordinates_lat__gte=lat - radius / 69 )\
            .filter(destination_coordinates_lon__lte=lon + radius / 50)\
            .filter(destination_coordinates_lon__gte=lon - radius / 50)

            recent_items = recent_items | close_items

        recent_items = recent_items[:200]

        #Gets all the different categories
        filters = RideCategory.objects.all()

        # Paginator will show 16 items per page
        paginator = Paginator(recent_items, 16, allow_empty_first_page=True)
        page = request.GET.get('page') # Gets the page number to display
        rides = paginator.get_page(page)

        #Puts all the data to be displayed into context
        context = {
          'rides': rides,
          'title': title,
          'search': request.GET['search'],
          'search_split': search_split,
          'filters': filters,
        }

        addErrorOnEmpty(context, 'SearchFail')

        #Returns a render function call to display onto the website for the user to see
        return render(request, template, context)

    #If the user is not logged in then they get redirected to the HuskyStatue screen
    else:
        return HttpResponseRedirect('/')

#This function allows a user to choose from a dropdown
#what category/ies of items they want to see
#param: request - array passed throughout a website, kinda like global variables
#returns: render function that changes the items the user sees based on the category/ies
def filter(request):
  #The CSS code for this function can be found here
  template = 'rideSharing/index.html'

    #The title for the webpage
  title = 'MTU Ridesharing'

    #Checks to make sure the user has logged in
  if request.user.is_authenticated:
    filters = RideCategory.objects.all()
    misform = False
    failed_search = None

    #Uses the filter function to get the data of the searched items based on filters
    recent_rides = RideItem.objects.all()
    if not request.GET.getlist('filter'):
      return HttpResponseRedirect('/rideSharing')
    for filt in request.GET.getlist('filter'):
      if len([x for x in filters if x.category_name == filt]) == 0:
        misform = True
      recent_rides = recent_rides.filter(
        archived='False',
        ride_category__category_name=filt
      ).order_by('-date_added')

    # Paginator will show 16 items per page
    paginator = Paginator(recent_rides, 16, allow_empty_first_page=True)
    page = request.GET.get('page') # Gets the page number to display
    rides = paginator.get_page(page)


    #Gets all the different categories
    curFilters = request.GET.getlist('filter')
        #Puts all the data to be displayed into context
    context = {
      'rides': rides,
      'title': title,
      'filters': filters,
      'curFilters': curFilters,
      'failed_search': failed_search
    }

    addErrorOnEmpty(context, 'FilterFail')
    if misform:
        context['failed_search'] = "MisformedFilterFail"

        #Returns a render function call to display onto the website for the user to see
    return render(request, template, context)

    #If the user is not logged in then they get redirected to the HuskyStatue screen
  else:
    return HttpResponseRedirect('/')
