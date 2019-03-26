from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from datetime import datetime

from .forms import SellingForm
from catalog.models import CatalogItem 

# Create your views here.
#class SellingListView(ListView):
#    model = CatalogItem 
#    contex_object_name = 'obj'
#
#class SellingCreateView(CreateView):
#    model = CatalogItem 
#    fields = ('item_title', 'item_description', 'item_price', 'category')
#    success_url = reverse_lazy('index')
#
#class SellingUpdateView(UpdateView):
#    model = CatalogItem 
#    fields = ('item_title', 'item_description', 'item_price', 'category')
#    success_url = reverse_lazy('index')


def index(request):
    template = 'selling/index.html'
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SellingForm(request.POST, request.FILES)
            if form.is_valid():
                category = form.cleaned_data['category']
                item_description = form.cleaned_data['item_description']
                item_price = form.cleaned_data['item_price']
                item_title = form.cleaned_data['item_title']
                username = request.user
                item_picture = form.cleaned_data['item_picture']
                catalogItem_instance = CatalogItem.objects.create(username=username, category=category, item_description=item_description, item_price=item_price, item_title=item_title, item_picture=item_picture)
                catalogItem_instance.save()
                return HttpResponseRedirect('/')

        else:
            form = SellingForm()
        context = {'form': form,}
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')

