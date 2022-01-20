from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from catalog.models import CatalogItem, Category
from rideSharing.models import RideItem
from catalog.views import isUserNotBanned
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

from profanity_check.profanityModels import ProfFiltered_ModelForm
from profanity_check.models import ArchivedType

# The HTML Form that's submitted on the Edit Account page
#   the ModelForm is used for data validation and automatic HTML production

class EditModelForm( ProfFiltered_ModelForm ):
    class Meta:
        model = user_profile
        fields = ['preferred_name', 'home_city', 'home_state', 'zipcode', 'picture', 'digest']
        widgets = {
            #'bio': Textarea(attrs={'rows': 5}),
            'picture': PreviewImageWidget()
        }

    def clean_preferred_name(self):
        return self.profanity_cleaner('preferred_name')

    def clean_home_city(self):
        return self.profanity_cleaner('home_city')

    def clean_home_state(self):
        return self.profanity_cleaner('home_state')


    def clean_picture(self):
        pic = self.cleaned_data['picture']
        if (pic != None and pic.size > settings.MAX_UPLOAD_SIZE):
            raise forms.ValidationError(_('Filesize is too large and image could not be automatically downsized: Please use a smaller or lower-resolution image. Maximum file size is: %(max_size).1f %(type)s'),
            params={'max_size': 1024**(math.log(settings.MAX_UPLOAD_SIZE, 1024)%1), 'type': ["B", "KB", "MB", "GB", "TB"][int(math.floor(math.log(settings.MAX_UPLOAD_SIZE, 1024)))] }, code='toolarge')
        return pic

# Handles both GET and POST requests for the user account edit page
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def edit(request):
    currentUser = user_profile.objects.get(user = request.user)

    if request.method == "POST":
        # Validate the data submitted
        form = EditModelForm(request.POST, request.FILES, instance = currentUser, override_text = "Submit Anyway" )#, profCheck = profCheck )

        if form.is_valid():
            # Check if the user clicked the 'reset' button last; if so, reset their picture
            if request.POST.get( PreviewImageWidget.reset_check_name(None, 'picture') ) == '1':
                currentUser.picture = None
                currentUser.save()

            form.save()
            return HttpResponseRedirect(reverse('accountant:index'))

    else: # ie request.method == "GET"
        form = EditModelForm(instance = currentUser)

    context = {
        'form': form,
    }

    # Either a GET or a failed POST end up here
    return render(request, 'accountant/account_detail.html', context)

# Redirect to the welcome page (this used to be the catalog)
def catalogRedirect(request):
    return HttpResponseRedirect('/welcome')

# Logout link
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

# Loads the primary account page
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def index(request):

    currentUser = user_profile.objects.get(user = request.user)
    template = 'accountant/index.html'
    defaultPicture = 'https://www.mtu.edu/mtu_resources/images/download-central/social-media/gold-name.jpg'

    # load items and rides
    my_items = CatalogItem.objects.filter(username = request.user).filter( ArchivedType.Q_myContent )
    ride_items = RideItem.objects.filter(username = request.user).filter( ArchivedType.Q_myContent )
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

@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def developer(request):
    current_token = Token.objects.filter(user = request.user).first()

    return render(request, 'accountant/developer_settings.html', {
        'current_token': current_token
    })

@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def developer_generate_token(request):

    current_token = Token.objects.filter(user = request.user).first()

    if current_token:
        current_token.delete()

    Token.objects.create(user = request.user)

    return HttpResponseRedirect('/accountant/developer')

# Used as an intermediate function to delete an item
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def deleteItem(request, pk):

    # delete item from database
    item = CatalogItem.objects.get(pk=pk)

    # delete only if this user owns the item, a precautionary measure
    if item.username == request.user:
      item.archived = "True" # archive this item
      item.archivedType = ArchivedType.Types.ARCHIVED
      item.save()


    # redirect to accountant page
    return HttpResponseRedirect('/accountant')

# Used as an intermediate function to delete an item
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def deleteRide(request, pk):
    
    # delete ride from database
    ride = RideItem.objects.get(pk=pk)

    # delete only if this user owns the ride, a precautionary measure
    if ride.username == request.user:
      ride.archived = "True" # archive this ride
      ride.archivedType = ArchivedType.Types.ARCHIVED
      ride.save()

    # redirect to accountant page (refresh)
    return HttpResponseRedirect('/accountant')
