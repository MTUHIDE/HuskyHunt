from PIL import Image
from django import forms
from catalog.models import CatalogItem, Category, CatalogItemPicture
from django.forms import ModelForm
from rideSharing.models import RideItem, RideCategory
from django.forms import TextInput
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import math
from datetime import date, timedelta
from profanity_check.profanityModels import ProfFiltered_ModelForm
from io import BytesIO
from django.core.files import File



#Defines the form to create an item
class SellingForm(ProfFiltered_ModelForm):

    class Meta:

        #The table that the information will go into
        model = CatalogItem

        #The "special" input areas
        widgets = {
                'item_description': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

        #The normal input areas
        fields = ('category', 'item_title', 'item_price', 'item_description')

    def __init__(self, *args, **kwargs):
        self._request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


        #Gets all the available categories for the new item
        self.fields['category'].queryset = Category.objects.all()

    def clean(self):
        super().clean()


        uplPos = self._request.POST.getlist('uplPos').copy()
        currUpl = self._request.POST.getlist('currUpl').copy()
        cleanedPics = []
        validationErrors = []
        for pic in self._request.FILES.getlist('curr_picture'):
            # please, god, deliver these unto me in source ordering
            #  despite not mentioning this feature anywhere in your holy texts, the Django docs,
            #   which I guess in this metaphor makes StackExchange the equivalent of rabbinic commentaries
            try:
                result = self._clean_a_picture(pic)
                if result is not None:
                    cleanedPics.append(result)
            except forms.ValidationError as e:
                validationErrors.append(e)
        if len(validationErrors) > 0:
            raise forms.ValidationError(validationErrors)
        if len(cleanedPics) + len(currUpl) == 0:
            raise forms.ValidationError( "At least one picture is needed!", code="empty")


        '''
        The loops are intertwined: uplPos is *only* for the preexisting images,
        which are already in the database. So the loops are combined because the
        position tracker i is updated after each step -- each loop *either*
        pulls in an already-uploaded image, *or* makes a new CatalogItemPicture,
        but either way the relevant position is assigned and i is incremented.
        '''
        self.otherPictures = self.instance.pictures
        self.specialPictures = []
        self.cleaned_data["pictures"] = []
        i = 1
        catpic = None
        while(1):
            if len(uplPos) > 0 and str(i) == uplPos[0]:
                uplPos.pop(0)
                pk = currUpl.pop(0)
                catpic = CatalogItemPicture.objects.get(pk=pk)     #item.pictures.filter
                self.otherPictures = self.otherPictures.exclude(pk=pk)
                self.specialPictures.append(catpic)
                catpic.position = i
            elif len(cleanedPics) > 0:
                catpic = CatalogItemPicture(picture=cleanedPics.pop(0), item=self.instance, position=i )
            else:
                break
            self.cleaned_data["pictures"].append(catpic)
            i += 1

    def save(self, commit=True):
        item = super().save(commit=False)

        if item.item_price < 0:
            item.item_price = 0
        item.username = self._request.user

        if commit:
            item.save()

            # we have to be careful about order here, because of the
            #  unique_together constraint and sqlite doesn't allow deferred
            for pic in self.otherPictures.all():
                pic.delete()    # clear out taken positions
            for pic in self.specialPictures:
                pic.position += 2*len(self.cleaned_data["pictures"])
                pic.save()  # move them up to guaranteed-untaken positions
            for pic in self.specialPictures:
                pic.position -= 2*len(self.cleaned_data["pictures"])
                pic.save()      # move still-around ones to new positions
            for pic in self.cleaned_data["pictures"]:
                pic.save()      # save everything

        return item

    def _clean_a_picture(self, pic):
        im = Image.open(pic)
        if im.format.lower() not in settings.ALLOWED_UPLOAD_IMAGES:
            raise forms.ValidationError(_("Unsupported file format. Supported formats are %s."
                                          % ", ".join(settings.ALLOWED_UPLOAD_IMAGES)))

        # create a BytesIO object
        im_io = BytesIO() 
        # save image to BytesIO object
        im.save(im_io, 'JPEG', quality=60) 
        # create a django-friendly Files object
        new_image = File(im_io, name=pic.name)

        if new_image.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(_('Filesize is too large and image could not be automatically downsized: Please use a smaller or lower-resolution image. Maximum file size is: %(max_size).1f %(type)s'),
            params={'max_size': 1024**(math.log(settings.MAX_UPLOAD_SIZE, 1024)%1), 'type': ["B", "KB", "MB", "GB", "TB"][int(math.floor(math.log(settings.MAX_UPLOAD_SIZE, 1024)))] }, code='toolarge')

        return new_image

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
