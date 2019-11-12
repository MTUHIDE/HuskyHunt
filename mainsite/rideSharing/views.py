from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.contrib import auth
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages

from django.forms import ModelForm
from rideSharing.models import RideItem
from django.views.generic.edit import CreateView
from accountant.models import user_profile
from django.urls import reverse

def index(request):

    #The CSS for this function can be found here
    template = 'rideSharing/index.html'
    #The title for the webpage
    title = "MTU Ridesharing"

    #Checks if the user is logged in
    if request.user.is_authenticated:
        #Call the CSS template to be displayed
        context = { 'items': RideItem.objects.filter(username = request.user) }
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')


class RideCreate(CreateView):
    model = RideItem
    fields = ['start_city', 'start_state', 'start_zipcode', 'destination_city', 'destination_state', 'destination_zipcode', 'date_leaving', 'round_trip', 'return_date', 'spots', 'driver', 'notes', 'price']
    #fields left out: username, views, date_added
    initial = {'start_city': "Houghton", 'start_state': "Michigan", 'start_zipcode': 49931}
    success_url = ''

    _this_user = None

    def setup(self, request, *args, **kwargs):
        self._this_user = user_profile.objects.get(user = request.user)
        self.initial['driver'] = self._this_user.preferred_name

        super().setup(request, args, kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = self._this_user.user
        self.object.views = 0

        #self.object.username = self._this_user.user
        #self.object.views = 0

        self.object.save()

        return HttpResponseRedirect(reverse('rideSharing:index'))
