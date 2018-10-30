from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    category_name = models.CharField(max_length=200)
    subcategory_of = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.category_name

class CatalogItem(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ManyToManyField(SubCategory)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    item_title = models.CharField(max_length=200)
    item_description = models.CharField(max_length=1500)
    item_picture = models.ImageField(upload_to='catalog/%Y/%m/%d/', height_field=None, width_field=None)
    item_price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.item_title
