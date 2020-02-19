import re   #eeeeee

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.contrib import auth
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages
from rideSharing.models import RideItem
from django import forms
from django.core.paginator import Paginator

#This function gets all the items from the database
#and displays them to the screen sorted by most recently added
#param: request - array variable that is passed around the website, kinda like global variables
#returns: all the items in the database, with the most recently item added at the top
def index(request):

    #The CSS for this function can be found here
    template = 'rideSharing/index.html'
    #The title for the webpage
    title = "MTU Ridesharing"

    #Checks if the user is logged in
    if request.user.is_authenticated:

        #Gets 500 most recent items from the database and sorts by date added
        recent_items = RideItem.objects.filter(
            date_added__lte=timezone.now()
        ).order_by('-date_added')[:500]

        # Paginator will show 16 items per page
        paginator = Paginator(recent_items, 16, allow_empty_first_page=True)
        page = request.GET.get('page') # Gets the page number to display
        rides = paginator.get_page(page)


        #Packages the information to be displayed into context
        context = {
            'title': title,
            'rides': rides,
            'search': 0,
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
            Q(notes__contains=request.GET['search'])
        )

        radius = 1
        crResults = re.match(r'\[\s*(\-?\d{1,3}(?:\.\d+)?)\s*\,\s*(\-?\d{1,3}(?:\.\d+)?)\s*\]', request.GET['search'])
        if(crResults is not None):
            lat = float(crResults.group(1))
            lon = float(crResults.group(2))

            close_items = RideItem.objects\
            .filter(destination_coordinates_lat__lte=lat+radius)\
            .filter(destination_coordinates_lat__gte=lat-radius)\
            .filter(destination_coordinates_lon__lte=lon+radius)\
            .filter(destination_coordinates_lon__gte=lon-radius)

            recent_items = recent_items | close_items

        recent_items = recent_items[:200]

        # Paginator will show 16 items per page
        paginator = Paginator(recent_items, 16, allow_empty_first_page=True)
        page = request.GET.get('page') # Gets the page number to display
        rides = paginator.get_page(page)

        #Puts all the data to be displayed into context
        context = {
          'rides': rides,
          'title': title,
          'search': request.GET['search'],
        }

        addErrorOnEmpty(context, 'SearchFail')

        #Returns a render function call to display onto the website for the user to see
        return render(request, template, context)

    #If the user is not logged in then they get redirected to the HuskyStatue screen
    else:
        return HttpResponseRedirect('/')
