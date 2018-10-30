from django import forms
from catalog.models import CatalogItem, Category, SubCategory

class SellingForm(forms.ModelForm):
    class Meta:
        model = CatalogItem 
        widgets = {
                'item_description': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        fields = ('category', 'item_title', 'item_price', 'item_description', 'item_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()


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
