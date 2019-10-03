from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.contrib import auth
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages

def index(request):

    #The CSS for this function can be found here
    template = 'rideSharing/index.html'
    #The title for the webpage
    title = "MTU Ridesharing"

    #Checks if the user is logged in
    if request.user.is_authenticated:
        #Call the CSS template to be displayed
        return render(request, template)
    else:
        return HttpResponseRedirect('/')