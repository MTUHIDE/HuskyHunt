from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Create your models here.

# class Account(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True)
#     street_address = models.CharField(max_length=200, blank=True)
#     city = models.CharField(max_length=100, blank=True)
#     zipcode = models.IntegerField(default=0, blank=True)
#     common_destination_zipcode = models.IntegerField(default=0, blank=True)
#     picture = models.ImageField(upload_to='account/profilepics/', height_field=None, width_field=None, blank=True, null=True)
#     rating = models.IntegerField(default=0)

#     USERNAME_FIELD = 'user'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.user.username

#     def is_anonymous(self):
#         return False

#     def get_short_name(self):
#         return self.user.username

#     def is_authenticated(self):
#         return True

class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_name = models.CharField(max_length=50, blank = True, null=True)
    home_city = models.CharField(max_length=50, blank = True, null=True)
    home_state = models.CharField(max_length=50, blank = True, null=True)
    zipcode = models.IntegerField(blank = True, null=True)
    picture = picture = models.ImageField(upload_to='account/profilepics/', height_field=None, width_field=None, blank = True, null=True)

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile.objects.create(user=instance)

class UserInLine(admin.StackedInline):
    model = user_profile
    can_delete = False
    verbose_name_plural = 'user_profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserInLine,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)