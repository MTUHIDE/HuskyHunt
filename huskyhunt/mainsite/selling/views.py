from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render

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
            form = SellingForm(request.POST)
            if form.is_valid():
                description = form.cleaned_data['description']
                price = form.cleaned_data['price']
                title = form.cleaned_data['title']
                return redirect('index')

        else:
            form = SellingForm()
        context = {'form': form,}
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')

