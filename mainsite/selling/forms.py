from django import forms
from catalog.models import CatalogItem, Category, SubCategory

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

