from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    street_address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zipcode = models.IntegerField(default=0, blank=True)
    common_destination_zipcode = models.IntegerField(default=0, blank=True)
    picture = models.ImageField(upload_to='account/profilepics/', height_field=None, width_field=None, blank=True, null=True)
    rating = models.IntegerField(default=0)

    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user.username

    def is_anonymous(self):
        return False

    def get_short_name(self):
        return self.user.username

    def is_authenticated(self):
        return True
