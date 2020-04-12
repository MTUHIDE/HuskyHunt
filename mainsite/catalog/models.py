from django.contrib.auth.models import User # imports the user table
from django.db import models
from django.conf import settings
from accountant.models import user_profile
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save


#Defines a table of categories
class Category(models.Model):
    #Each category has a name, date the category was created, and date of last update

    #The name can be up to 200 letters in length
    category_name = models.CharField(max_length=200)

    #The date created is automatically filled in with the current date
    date_created = models.DateField(auto_now=False, auto_now_add=True)

    #The date updated is automatically filled in with the current date and time
    date_updated = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.category_name

#Defines a table of subcategories
class SubCategory(models.Model):
    #Each subcategory has a name, parent category, date of creation and the last update

    #The subcategory name can be up to 200 letters in length
    category_name = models.CharField(max_length=200)

    #The subcategory is tied to one of the main categories
    #and is deleted if the parent is deleted
    subcategory_of = models.ForeignKey(Category, on_delete=models.CASCADE)

    #The date created is automatically filled in with the current date
    date_created = models.DateField(auto_now=False, auto_now_add=True)

    #The date updated is automatically filled in with the current date and time
    date_updated = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.category_name

#Defines a table of Items
class CatalogItem(models.Model):
    #Each item has a username, category, subcategory, date added, title, description
    #picture, and price associated to it

    #The username is automatically set to the user that added the item
    #and the item is deleted if the user is deleted
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    #The preferred name of the item in question;
    # note, I'm unsure of the performance implications of making this query all the time
    def get_preferred_first_name(self):
        try:
            user = user_profile.objects.get(user=self.username)
        except user_profile.DoesNotExist:
            return self.username
        name = user.preferred_name
        if not name or name == "":
            name = self.username.first_name
        return name
    first_name = property(get_preferred_first_name)

    #The category is set by the user and the item is deleted if its category is deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    #The item has a subcategory that I don't believe does anything
    subcategory = models.ManyToManyField(SubCategory)

    #The date added is automatically set to the current date and time
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)

    #The name of the item, can be up to 200 letters long
    item_title = models.CharField(max_length=200)

    #A description of the item that can be 1500 letters long
    item_description = models.CharField(max_length=1500, blank=True)

    #Picture that is uploaded on item creation
    item_picture = models.ImageField(upload_to='catalog/%Y/%m/%d/', height_field=None, width_field=None)

    #The price that the user wants to sell the item at
    item_price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    #An integer identifying the item
    views = models.IntegerField(default=0)

    # If the ride has been archived or not
    archived = models.BooleanField(default=False)

    # If the ride is currently reported (flagged to be reviewed) or not
    reported = models.BooleanField(default=False)

    def __str__(self):
        return self.item_title

    def __getName__(self):
        return self.username.first_name

@receiver(post_delete, sender=CatalogItem)
def delete_ondelete_photos(sender, instance, **kwargs):
    if instance.item_picture:
        instance.item_picture.delete(save=False)

#Below is untested because, at the time of this comment, we have no 'edit item' form
@receiver(pre_save, sender=CatalogItem)
def delete_changed_photos(sender, instance, **kwargs):
    try:
        item = CatalogItem.objects.get(pk=instance.pk)
    except CatalogItem.DoesNotExist:
        return #
    if not instance.item_picture == item.item_picture:
        item.item_picture.delete(save=False)

