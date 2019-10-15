#from django.views.generic import ListView, CreateView, UpdateView
#from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import AccountForm
from .models import Account
from django.contrib import auth
from catalog.models import CatalogItem, Category, SubCategory
from django.utils import timezone
# Create your views here.
#class AccountListView(ListView):
#    model = Account
#    contex_object_name = 'obj'
#
#class AccountCreateView(CreateView):
#    model = Account
#    fields = ('item_title', 'item_description', 'item_price', 'category')
#    success_url = reverse_lazy('index')
#
#class AccountUpdateView(UpdateView):
#    model = Account
#    fields = ('item_title', 'item_description', 'item_price', 'category')
#    success_url = reverse_lazy('index')


def catalogRedirect(request):
    return HttpResponseRedirect('/catalog')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def index(request):
   template = 'accountant/index.html'
   defaultPicture= 'default-profile.gif'

   if request.user.is_authenticated:
      recent_items = CatalogItem.objects.filter(
         date_added__lte=timezone.now()
      ).order_by('-date_added')[:5]
      filters = Category.objects.all()
      context = {
         'item_list': recent_items,
         'filters': filters,
         'defaultPicture':defaultPicture,
      }
      return render(request, template, context)
   else:
      return HttpResponseRedirect('/')
