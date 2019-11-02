#from django.views.generic import ListView, CreateView, UpdateView
#from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import AccountForm
from .models import Account
from django.contrib import auth
from catalog.models import CatalogItem, Category, SubCategory
from django.utils import timezone
from django.urls import reverse

from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from django.forms import ModelForm


class EditModelForm(ModelForm):
    class Meta:
        model = Account
        fields = ['bio', 'street_address', 'city', 'zipcode', 'common_destination_zipcode', 'picture']

def edit(request):
    try:
        currentUser = Account.objects.get(user = request.user)
    except Account.DoesNotExist:
        createDefaultAccount(request.user)
        currentUser = Account.objects.get(user = request.user)

    if request.method == "POST":
        form = EditModelForm(request.POST, request.FILES, instance = currentUser)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accountant:index'))
    else: # request.method == "GET"
        form = EditModelForm(instance = currentUser)
    return render(request, 'accountant/account_detail.html', {'form': form})


def catalogRedirect(request):
    return HttpResponseRedirect('/catalog')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def index(request):
   if request.user.is_authenticated:
      template = 'accountant/index.html'
      defaultPicture= 'https://www.mtu.edu/mtu_resources/images/download-central/social-media/gold-name.jpg'
      my_items = CatalogItem.objects.filter(username = request.user)
      filters = Category.objects.all()
      title = 'My items'
      context = {
                  'item_list':my_items,
                  'title': title,
                  'filters': filters,
                  'defaultPicture': defaultPicture,
        }
      return render(request, template, context)
   else:
      return HttpResponseRedirect('/')

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
