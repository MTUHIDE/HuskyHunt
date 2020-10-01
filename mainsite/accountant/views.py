from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from catalog.models import CatalogItem, Category, SubCategory
from rideSharing.models import RideItem
from rest_framework.authtoken.models import Token
from django.utils import timezone

from accountant.models import user_profile
from django.db.models import Q
from django.contrib.auth.models import User

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import math

from django.urls import reverse
from django.forms import ModelForm

from .widgets import PreviewImageWidget


# The HTML Form that's submitted on the Edit Account page
#   the ModelForm is used for data validation and automatic HTML production

class EditModelForm(ModelForm):
    class Meta:
        model = user_profile
        fields = ['preferred_name', 'home_city', 'home_state', 'zipcode', 'picture']
        widgets = {
            #'bio': Textarea(attrs={'rows': 5}),
            'picture': PreviewImageWidget()
        }

    def clean_picture(self):
        pic = self.cleaned_data['picture']
        if pic.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(_('Filesize is too large and image could not be automatically downsized: Please use a smaller or lower-resolution image. Maximum file size is: %(max_size).1f %(type)s'),
            params={'max_size': 1024**(math.log(settings.MAX_UPLOAD_SIZE, 1024)%1), 'type': ["B", "KB", "MB", "GB", "TB"][int(math.floor(math.log(settings.MAX_UPLOAD_SIZE, 1024)))] }, code='toolarge')
        return pic

# Handles both GET and POST requests for the user account edit page
def edit(request):
    currentUser = user_profile.objects.get(user = request.user)

    if request.method == "POST":
        # Check if the user clicked the 'reset' button last; if so, reset their picture
        if request.POST.get( PreviewImageWidget.reset_check_name(None, 'picture') ) == '1':
            currentUser.picture = None

        # Validate the data submitted
        form = EditModelForm(request.POST, request.FILES, instance = currentUser)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accountant:index'))

    else: # ie request.method == "GET"
        form = EditModelForm(instance = currentUser)

    # Either a GET or a failed POST end up here
    return render(request, 'accountant/account_detail.html', {'form': form})

# Redirect to the welcome page (this used to be the catalog)
def catalogRedirect(request):
    return HttpResponseRedirect('/welcome')

# Logout link
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

# Loads the primary account page
def index(request):

    if request.user.is_authenticated:
        currentUser = user_profile.objects.get(user = request.user)
        template = 'accountant/index.html'
        defaultPicture = 'https://www.mtu.edu/mtu_resources/images/download-central/social-media/gold-name.jpg'

        # load items and rides
        my_items = CatalogItem.objects.filter(username = request.user, archived='False')
        ride_items = RideItem.objects.filter(username = request.user, archived='False')
        filters = Category.objects.all()
        title = 'My items'

      # Put data in context to be accessed from template
        context = {
            'item_list':my_items,
            'ride_list':ride_items,
            'title': title,
            'filters': filters,
            'defaultPicture': currentUser.picture.url if currentUser.picture else defaultPicture,
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')

def developer(request):
    if request.user.is_authenticated:
        current_token = Token.objects.filter(user = request.user).first()

        return render(request, 'accountant/developer_settings.html', {
            'current_token': current_token
        })
    else:
        return HttpResponseRedirect('/')

def developer_generate_token(request):
    if request.user.is_authenticated:
        current_token = Token.objects.filter(user = request.user).first()

        if current_token:
            current_token.delete()

        Token.objects.create(user = request.user)

    else:
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/accountant/developer')

# Used as an intermediate function to delete an item
def deleteItem(request, pk):
  if request.user.is_authenticated:
    # delete item from database
    item = CatalogItem.objects.get(pk=pk)

    # delete only if this user owns the item, a precautionary measure
    if item.username == request.user:
      item.archived = "True" # archive this item
      item.save()


    # redirect to accountant page
    return HttpResponseRedirect('/accountant')
  else:
    return HttpResponseRedirect('/')

# Used as an intermediate function to delete an item
def deleteRide(request, pk):
  if request.user.is_authenticated:
    # delete ride from database
    ride = RideItem.objects.get(pk=pk)

    # delete only if this user owns the ride, a precautionary measure
    if ride.username == request.user:
      ride.archived = "True" # archive this ride
      ride.save()

    # redirect to accountant page (refresh)
    return HttpResponseRedirect('/accountant')
  else:
    return HttpResponseRedirect('/')
