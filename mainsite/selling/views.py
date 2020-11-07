import requests

from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from catalog.views import isUserNotBanned
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime

from .forms import SellingForm
from catalog.models import CatalogItem

from django.urls import reverse
from django.views.generic.edit import CreateView
from .forms import RideForm
from rideSharing.models import RideItem
from accountant.models import user_profile


@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def index(request):
    
    template = "selling/combine.html"
    catalog_form = None
    ride_form = None

    if request.method == 'POST':
        post_request = request.POST.copy() #make it not immutable

        # Ride Form
        submission_type = post_request.pop('submission_type', None)
        if submission_type == ['ride'] and 4 >= RideItem.objects.filter(username = request.user, archived='False').count():
            ride_form = RideForm(post_request, request.FILES)
            if ride_form.is_valid():
                ride_item = ride_form.save(commit=False)
                ride_item.username = request.user
                ride_item.views = 0
                if (ride_item.price < 0):
                    ride_item.price = 0

                ride_item.destination_coordinates_lat, ride_item.destination_coordinates_lon = getLocationByRequest(ride_item)
                ride_item.start_coordinates_lat, ride_item.start_coordinates_lon = getStartByRequest(ride_item)

                ride_item.save()       #error?

                # Inrement number of points by one
                profile = user_profile.objects.get(user = request.user)
                profile.points = profile.points + 1
                profile.save()

                # check for failure cases! what happens with invalid data?
                return HttpResponseRedirect(reverse('rideSharing:index'))

        # Catalog Form
        elif submission_type == ['ctlg'] and 10 >= CatalogItem.objects.filter(username = request.user, archived='False').count():
            catalog_form = SellingForm(post_request, request.FILES)
            if catalog_form.is_valid():
                category = catalog_form.cleaned_data['category']
                item_description = catalog_form.cleaned_data['item_description']
                item_price = catalog_form.cleaned_data['item_price']
                if item_price < 0:
                    item_price = 0
                item_title = catalog_form.cleaned_data['item_title']
                username = request.user
                item_picture = catalog_form.cleaned_data['item_picture']
                catalogItem_instance = CatalogItem.objects.create(username=username, category=category, item_description=item_description, item_price=item_price, item_title=item_title, item_picture=item_picture)
                catalogItem_instance.save()

                # Inrement number of points by one
                profile = user_profile.objects.get(user = request.user)
                profile.points = profile.points + 1
                profile.save()

                return HttpResponseRedirect(reverse('catalog:index'))
        else:
            pass #this should never happen

    if catalog_form is None and 10 >= CatalogItem.objects.filter(username = request.user, archived='False').count():
        catalog_form = SellingForm()
    if ride_form is None and 4 >= RideItem.objects.filter(username = request.user, archived='False').count():
        curr_user = user_profile.objects.get(user = request.user)
        ride_form = RideForm(initial = {
            'start_city': "Houghton",
            'start_state': "Michigan",
            'start_zipcode': 49931,
            'destination_city': curr_user.home_city,
            'destination_state': curr_user.home_state,
            'destination_zipcode': curr_user.zipcode,
            'driver': curr_user.preferred_name if curr_user.preferred_name else request.user.get_short_name()
        })

    # Set to true if the user has more than 10 items
    too_many_items = False;
    if catalog_form is None:
        too_many_items = True;

    # Set to true if the user has more than 4 rides
    too_many_rides = False;
    if ride_form is None:
        too_many_rides = True;

    context = {
        'catalog_form': catalog_form,
        'ride_form': ride_form,
        'too_many_items': too_many_items,
        'too_many_rides': too_many_rides,
    }
    return render(request, template, context)


def getLocationByRequest(ride_item):
        access_token = 'pk.eyJ1IjoiY3NjaHdhIiwiYSI6ImNrNjZxdmdsYTE5MGUzbG84Z3N1dTUzOTcifQ.DKfzMNPM0XvkkwJ-nLQDHg'

        destination_city = ride_item.destination_city
        destination_state = ride_item.destination_state
        destination_zipcode = ride_item.destination_zipcode

        locate_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/" \
        + requests.utils.quote(destination_city.strip()) + "%20" \
        + requests.utils.quote(destination_state.strip()) + "%20" \
        + requests.utils.quote(destination_zipcode.strip()) + "%20" \
        + ".json?access_token=" + access_token;

        req = requests.get(locate_url)

        lon, lat = (req.json())["features"][0]["center"]
        return lat, lon;

def getStartByRequest(ride_item):
        access_token = 'pk.eyJ1IjoiY3NjaHdhIiwiYSI6ImNrNjZxdmdsYTE5MGUzbG84Z3N1dTUzOTcifQ.DKfzMNPM0XvkkwJ-nLQDHg'

        start_city = ride_item.start_city
        start_state = ride_item.start_state
        start_zipcode = ride_item.start_zipcode

        locate_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/" \
        + requests.utils.quote(start_city.strip()) + "%20" \
        + requests.utils.quote(start_state.strip()) + "%20" \
        + requests.utils.quote(start_zipcode.strip()) + "%20" \
        + ".json?access_token=" + access_token;

        req = requests.get(locate_url)

        lon, lat = (req.json())["features"][0]["center"]
        return lat, lon;
