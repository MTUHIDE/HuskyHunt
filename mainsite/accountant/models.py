from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils import timezone

upload_directory = 'account/profilepics/'


def validate_zip(value):
    try:
        int(value)
    except ValueError:
        raise ValidationError(
            '%(value)s is not a valid zip',
            params={'value': value},
        )


STATE_CHOICES = [
    ('Alabama', 'Alabama'),
    ('Alaska', 'Alaska'),
    ('Arizona', 'Arizona'),
    ('Arkansas', 'Arkansas'),
    ('California', 'California'),
    ('Colorado', 'Colorado'),
    ('Connecticut', 'Connecticut'),
    ('Delaware', 'Delaware'),
    ('Florida', 'Florida'),
    ('Georgia', 'Georgia'),
    ('Hawaii', 'Hawaii'),
    ('Idaho', 'Idaho'),
    ('Illinois', 'Illinois'),
    ('Indiana', 'Indiana'),
    ('Iowa', 'Iowa'),
    ('Kansas', 'Kansas'),
    ('Kentucky', 'Kentucky'),
    ('Louisiana', 'Louisiana'),
    ('Maine', 'Maine'),
    ('Maryland', 'Maryland'),
    ('Massachusetts', 'Massachusetts'),
    ('Michigan', 'Michigan'),
    ('Minnesota', 'Minnesota'),
    ('Mississippi', 'Mississippi'),
    ('Missouri', 'Missouri'),
    ('Montana', 'Montana'),
    ('Nebraska', 'Nebraska'),
    ('Nevada', 'Nevada'),
    ('New Hampshire', 'New Hampshire'),
    ('New Jersey', 'New Jersey'),
    ('New Mexico', 'New Mexico'),
    ('New York', 'New York'),
    ('North Carolina', 'North Carolina'),
    ('North Dakota', 'North Dakota'),
    ('Ohio', 'Ohio'),
    ('Oklahoma', 'Oklahoma'),
    ('Oregon', 'Oregon'),
    ('Pennsylvania', 'Pennsylvania'),
    ('Rhode Island', 'Rhode Island'),
    ('South Carolina', 'South Carolina'),
    ('South Dakota', 'South Dakota'),
    ('Tennessee', 'Tennessee'),
    ('Texas', 'Texas'),
    ('Utah', 'Utah'),
    ('Vermont', 'Vermont'),
    ('Virginia', 'Virginia'),
    ('Washington', 'Washington'),
    ('West Virginia', 'West Virginia'),
    ('Wisconsin', 'Wisconsin'),
    ('Wyoming', 'Wyoming')
]


class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_name = models.CharField(max_length=50, blank=True, null=True)
    home_city = models.CharField(max_length=50, blank=True, null=True)
    home_state = models.CharField(max_length=50, blank=True, choices=STATE_CHOICES, null=True)
    zipcode = models.CharField(blank=True, null=True, max_length=5, validators=[validate_zip, MinLengthValidator(5)])
    picture = models.ImageField(upload_to=upload_directory, height_field=None, width_field=None, blank=True, null=True)
    last_email = models.DateTimeField(null=True, auto_now_add=False)
    emails_today = models.IntegerField(blank=False, null=False, default=0)
    last_flag = models.DateTimeField(null=True, auto_now_add=False)
    flags_today = models.IntegerField(blank=False, null=False, default=0)
    points = models.IntegerField(blank=False, null=False, default=0)
    banned_until = models.DateTimeField(null=True, auto_now_add=False)
    digest = models.BooleanField(default=True)
    lastDigest = models.DateTimeField(null=False,default=timezone.now)

    def __str__(self):
        return self.user.username


@receiver(pre_save, sender=user_profile)
def delete_changed_photos(sender, instance, **kwargs):
    try:
        user = user_profile.objects.get(pk=instance.pk)
    except user_profile.DoesNotExist:
        return  #
    if not instance.picture == user.picture:
        user.picture.delete(save=False)


# Below is untested because, at the time of this comment, we have no deleting users (I think?)
@receiver(post_delete, sender=user_profile)
def delete_ondelete_photos(sender, instance, **kwargs):
    if instance.picture:
        instance.picture.delete(save=False)


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
