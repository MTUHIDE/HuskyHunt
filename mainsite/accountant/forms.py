from django import forms
from .models import Account 

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        widgets = {
                'bio': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        fields = ('picture', 'street_address', 'city', 'zipcode', 'common_destination_zipcode',)


#class SellingForm(forms.Form):
#    title = forms.CharField(max_length=30)
#    price = forms.DecimalField(max_digits=7, decimal_places=2)
#    long_description = forms.CharField(widget=forms.Textarea(attrs={
#        'placeholder': 'Item Description',
#        'class': 'form-control'
#        }),
#        label='Description',
#        max_length=500
#    )
#    image = forms.ImageField()
