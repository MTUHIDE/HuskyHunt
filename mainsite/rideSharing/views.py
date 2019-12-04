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
        }

        #Displays all the items from the database with repect to the CSS template
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')
