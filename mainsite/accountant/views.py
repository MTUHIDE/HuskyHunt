#from django.views.generic import ListView, CreateView, UpdateView
#from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import AccountForm
from .models import Account
from django.contrib import auth
from catalog.models import CatalogItem, Category, SubCategory
from django.utils import timezone

from django.views.generic import DetailView
from django.contrib.auth.models import User

class AccountDetailView(DetailView):
    model = Account
    context_object_name = "account"

    def get_object(self, queryset=None):
        try:
            return Account.objects.get(user = self.request.user)
        except Account.DoesNotExist:
            createDefaultAccount(request.user)
            return Account.objects.get(user = self.request.user)

def createDefaultAccount(user):
    acct = Account(user = user)
    acct.save()


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
