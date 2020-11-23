from PIL import Image
from django import forms
from catalog.models import CatalogItem, Category, SubCategory
from django.forms import ModelForm
from rideSharing.models import RideItem, RideCategory
from django.forms import TextInput
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import math
from datetime import date, timedelta

from profanity_check.profanityModels import ProfFiltered_ModelForm


#Defines the form to create an item
class SellingForm( ProfFiltered_ModelForm ):
    class Meta:

        #The table that the information will go into
        model = CatalogItem

        #The "special" input areas
        widgets = {
                'item_description': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

        #The normal input areas
        fields = ('category', 'item_title', 'item_price', 'item_description', 'item_picture')

    def __init__(self, *args, **kwargs):
        self._request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


        #Gets all the available categories for the new item
        self.fields['category'].queryset = Category.objects.all()

    def save(self, commit=True):
        item = super().save(commit=False)

        if item.item_price < 0:
            item.item_price = 0
        item.username = self._request.user

        if commit:
            item.save()
        return item

    def clean_item_picture(self):
        pic = self.cleaned_data['item_picture']
        if pic.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(_('Filesize is too large and image could not be automatically downsized: Please use a smaller or lower-resolution image. Maximum file size is: %(max_size).1f %(type)s'),
            params={'max_size': 1024**(math.log(settings.MAX_UPLOAD_SIZE, 1024)%1), 'type': ["B", "KB", "MB", "GB", "TB"][int(math.floor(math.log(settings.MAX_UPLOAD_SIZE, 1024)))] }, code='toolarge')

        im = Image.open(pic)

        if im.format.lower() not in settings.ALLOWED_UPLOAD_IMAGES:
            raise forms.ValidationError(_("Unsupported file format. Supported formats are %s."
                                          % ", ".join(settings.ALLOWED_UPLOAD_IMAGES)))

        return pic

    def clean_item_price(self):
        price = self.cleaned_data['item_price']
        if price < 0:
            raise forms.ValidationError(_('Price cannot be negative!'))
        return price

    def clean_item_title(self):
        return self.profanity_cleaner('item_title')

    def clean_item_description(self):
        return self.profanity_cleaner('item_description')


class RideForm( ProfFiltered_ModelForm ):
    class Meta:
        #The table that the information will go into
        model = RideItem

        # The normal input areas
        fields = ['ride_category', 'start_city', 'start_state', 'start_zipcode', 'destination_city', 'destination_state', 'destination_zipcode', 'date_leaving', 'round_trip', 'return_date', 'spots', 'driver', 'notes', 'price']

        #The "special" input areas
        widgets = {
            'driver': TextInput(attrs={'readonly': 'readonly'}),
            'notes': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'date_leaving': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'})
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            #Gets all the available categories for the new item
            self.fields['category'].queryset = RideCategory.objects.all()

    def clean_driver(self):
        return self.profanity_cleaner('driver')

    def clean_notes(self):
        return self.profanity_cleaner('notes')

    def clean_start_city(self):
        return self.profanity_cleaner('start_city')

    def clean_start_state(self):
        return self.profanity_cleaner('start_state')

    def clean_destination_city(self):
        return self.profanity_cleaner('destination_city')

    def clean_destination_state(self):
        return self.profanity_cleaner('destination_state')


    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError(_('Price cannot be negative!'))
        return price

    def clean_spots(self):
        spots = self.cleaned_data['spots']
        if spots <= 0:
            raise forms.ValidationError(_('You must offer at least one spot!'))
        if spots > 8:
            raise forms.ValidationError(_('Please offer 8 or less spots!'))
        return spots

    def clean_date_leaving(self):
        leaveDate = self.cleaned_data['date_leaving']
        today = date.today()

        if leaveDate < today:
            raise forms.ValidationError(_('You must leave today or in the future!'))

        return leaveDate

    def clean_return_date(self):

        # Return Date is Entered
        if (self.cleaned_data['return_date']):
            returnDate = self.cleaned_data['return_date']
            today = date.today()

            # Check if return date is less than today
            if returnDate < today:
                raise forms.ValidationError(_('You must return today or in the future!'))

            return returnDate

        # No date entered, check if this must be a round trip
        if (self.cleaned_data['round_trip'] == 1):
            raise forms.ValidationError(_('You must enter a valid return date for a round trip!'))

    def clean(self):
        cleaned_data = super().clean()

        # Return date is entered and it is a round_trip
        if (cleaned_data.get('return_date') and cleaned_data.get('round_trip') == 1):
            returnDate = cleaned_data.get('return_date')
            leaveDate = cleaned_data.get('date_leaving')
            today = date.today()

            # Add 5 weeks from leave date
            maxDate = leaveDate + timedelta(days=35)

            # Check if return date is more than 1 month after leaving
            if returnDate > maxDate:
                self.add_error('return_date', "You must return within 5 weeks after leaving!")

            # Check if return date is before leave date
            if returnDate < leaveDate:
                self.add_error('return_date', "You must return on a date after leaving!")

        return self.cleaned_data
