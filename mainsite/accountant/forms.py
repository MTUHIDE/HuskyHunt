from django import forms
from .models import Account 

#Defines the form for a user to input their account data
class AccountForm(forms.ModelForm):
    class Meta:
        #What table will the information be going into
        model = Account

        #The "special" input areas
        widgets = {
                'bio': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        
        #The normal input areas
        fields = ('picture', 'street_address', 'city', 'zipcode', 'common_destination_zipcode',)

