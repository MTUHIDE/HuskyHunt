from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from datetime import datetime

from .forms import SellingForm
from catalog.models import CatalogItem

from django.urls import reverse
from django.views.generic.edit import CreateView
from .forms import RideForm
from rideSharing.models import RideItem
from accountant.models import user_profile


# -------------------------------------------------------------
# Catalog view
# -------------------------------------------------------------


def catalog_item_form(request):
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
                return HttpResponseRedirect(reverse('catalog:index'))

        else:
            form = SellingForm()
        context = {'form': form,}
        return render(request, template, context)
    else:
        return HttpResponseRedirect(reverse('catalog:index'))

# -------------------------------------------------------------
# Ridesharing view
# -------------------------------------------------------------


class RideCreate(CreateView):
    model = RideItem
    form_class = RideForm

    initial = {'start_city': "Houghton", 'start_state': "Michigan", 'start_zipcode': 49931}
    success_url = ''

    _this_user = None

    def setup(self, request, *args, **kwargs):
        self._this_user = user_profile.objects.get(user = request.user)
        self.initial['destination_city'] = self._this_user.home_city
        self.initial['destination_state'] = self._this_user.home_state
        self.initial['destination_zipcode'] = self._this_user.zipcode


        if self._this_user.preferred_name:
            # use user's preferred name if exists
            self.initial['driver'] = self._this_user.preferred_name
        else:
            self.initial['driver'] = request.user.get_short_name();

        super().setup(request, args, kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = self._this_user.user
        self.object.views = 0

        self.object.save()

        return HttpResponseRedirect(reverse('rideSharing:index'))
