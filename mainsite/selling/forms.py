from django import forms
from catalog.models import CatalogItem, Category, SubCategory
from django.forms import ModelForm
from rideSharing.models import RideItem
from django.forms import TextInput


#Defines the form to create an item
class SellingForm(forms.ModelForm):
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
        super().__init__(*args, **kwargs)

        #Gets all the available categories for the new item
        self.fields['category'].queryset = Category.objects.all()


class RideForm(ModelForm):
    class Meta:
        model = RideItem
        fields = ['start_city', 'start_state', 'start_zipcode', 'destination_city', 'destination_state', 'destination_zipcode', 'date_leaving', 'round_trip', 'return_date', 'spots', 'driver', 'notes', 'price']
        widgets = {'driver': TextInput(attrs={'readonly': 'readonly'})}
