from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from catalog.models import CatalogItem, Category, SubCategory
from django.utils import timezone

from accountant.models import user_profile
from django.db.models import Q
from django.contrib.auth.models import User

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

# Handles both GET and POST requests for the user account edit page
def edit(request):
    currentUser = user_profile.objects.get(user = request.user)

    if request.method == "POST":
        # Check if the user clicked the 'reset' button last; if so, reset their picture
        if request.POST.get( PreviewImageWidget.reset_check_name(None, 'picture') ) is '1':
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

# Redirect to main catalog page
def catalogRedirect(request):
    return HttpResponseRedirect('/catalog')

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
        my_items = CatalogItem.objects.filter(username = request.user)
        filters = Category.objects.all()
        title = 'My items'

      # Put data in context to be accessed from template
        context = {
            'item_list':my_items,
            'title': title,
            'filters': filters,
            'defaultPicture': currentUser.picture.url if currentUser.picture else defaultPicture,
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')

# Used as an intermediate function to delete an item
def deleteItem(request, pk):
  if request.user.is_authenticated:
    # delete item from database
    item = CatalogItem.objects.filter(pk=pk)

    # delete only if this user owns the item, a precautionary measure
    if item.get(pk=pk).username == request.user:
      item.delete();

    # redirect to accountant page
    return HttpResponseRedirect('/accountant')
  else:
    return HttpResponseRedirect('/')
