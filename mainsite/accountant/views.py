from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from catalog.models import CatalogItem, Category, SubCategory
from django.utils import timezone
from accountant.models import user_profile
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.

# Redirect to main catalog page
def catalogRedirect(request):
    return HttpResponseRedirect('/catalog')

# Logout link
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

# Loads the primary account page
def index(request):
  # Check if user is authenticated
  if request.user.is_authenticated:
      # Gather all of the resources the template uses
      template = 'accountant/index.html'
      defaultPicture= 'https://www.mtu.edu/mtu_resources/images/download-central/social-media/gold-name.jpg'
      my_items = CatalogItem.objects.filter(username = request.user)
      filters = Category.objects.all()
      title = 'My items'

      # Put data in context to be accessed from template
      context = {
                  'item_list':my_items,
                  'title': title,
                  'filters': filters,
                  'defaultPicture': defaultPicture
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
