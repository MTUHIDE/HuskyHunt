from django.contrib.auth.models import User
from accountant.models import user_profile
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from profanity_check.models import ArchivedType
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accountant', '0004_auto_20210924_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='home_state',
            field=models.CharField(blank=True,
                                   choices=[('Alabama', 'Alabama'), ('Alaska', 'Alaska'), ('Arizona', 'Arizona'),
                                            ('Arkansas', 'Arkansas'), ('California', 'California'),
                                            ('Colorado', 'Colorado'), ('Connecticut', 'Connecticut'),
                                            ('Delaware', 'Delaware'), ('Florida', 'Florida'), ('Georgia', 'Georgia'),
                                            ('Hawaii', 'Hawaii'), ('Idaho', 'Idaho'), ('Illinois', 'Illinois'),
                                            ('Indiana', 'Indiana'), ('Iowa', 'Iowa'), ('Kansas', 'Kansas'),
                                            ('Kentucky', 'Kentucky'), ('Louisiana', 'Louisiana'), ('Maine', 'Maine'),
                                            ('Maryland', 'Maryland'), ('Massachusetts', 'Massachusetts'),
                                            ('Michigan', 'Michigan'), ('Minnesota', 'Minnesota'),
                                            ('Mississippi', 'Mississippi'), ('Missouri', 'Missouri'),
                                            ('Montana', 'Montana'), ('Nebraska', 'Nebraska'), ('Nevada', 'Nevada'),
                                            ('New Hampshire', 'New Hampshire'), ('New Jersey', 'New Jersey'),
                                            ('New Mexico', 'New Mexico'), ('New York', 'New York'),
                                            ('North Carolina', 'North Carolina'), ('North Dakota', 'North Dakota'),
                                            ('Ohio', 'Ohio'), ('Oklahoma', 'Oklahoma'), ('Oregon', 'Oregon'),
                                            ('Pennsylvania', 'Pennsylvania'), ('Rhode Island', 'Rhode Island'),
                                            ('South Carolina', 'South Carolina'), ('South Dakota', 'South Dakota'),
                                            ('Tennessee', 'Tennessee'), ('Texas', 'Texas'), ('Utah', 'Utah'),
                                            ('Vermont', 'Vermont'), ('Virginia', 'Virginia'),
                                            ('Washington', 'Washington'), ('West Virginia', 'West Virginia'),
                                            ('Wisconsin', 'Wisconsin'), ('Wyoming', 'Wyoming')], max_length=50,
                                   null=True),
        ),
    ]


# Defines a table of categories
class RideCategory(models.Model):
    # Each category has a name, date the category was created, and date of last update

    # The name can be up to 200 letters in length
    category_name = models.CharField(max_length=200)

    # The date created is automatically filled in with the current date
    date_created = models.DateField(auto_now=False, auto_now_add=True)

    # The date updated is automatically filled in with the current date and time
    date_updated = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.category_name


# Defines a table of Items
class RideItem(models.Model):
    # Internal Fields:
    # The username is automatically set to the user that added the item
    # and the item is deleted if the user is deleted
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # The preferred name of the item in question;
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

    # An integer identifying the ride, auto increments
    views = models.IntegerField(default=0)

    # The date added is automatically set to the current date and time, used for sorting purposes
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)

    # The category is set by the user and the item is deleted if its category is deleted
    ride_category = models.ForeignKey(RideCategory, on_delete=models.CASCADE)

    # Ride Fields:
    # City leaving from
    start_city = models.CharField(max_length=25)

    # State leaving from - OPTIONAL
    start_state = models.CharField(max_length=50, blank=True, choices=STATE_CHOICES, null=True)

    # Zipcode leaving from - OPTIONAL
    start_zipcode = models.CharField(blank=True, null=True, max_length=5,
                                     validators=[validate_zip, MinLengthValidator(5)])

    # City going to
    destination_city = models.CharField(max_length=25)

    # State going to - OPTIONAL
    destination_state = models.CharField(max_length=50, blank=True, choices=STATE_CHOICES, null=True)

    # Zipcode going to - OPTIONAL
    destination_zipcode = models.CharField(blank=True, null=True, max_length=5,
                                           validators=[validate_zip, MinLengthValidator(5)])

    # Calculated based on the previous points
    destination_coordinates_lat = models.DecimalField(decimal_places=6, max_digits=14, default=0.00)
    destination_coordinates_lon = models.DecimalField(decimal_places=6, max_digits=14, default=0.00)

    # Calculated based on the previous points
    start_coordinates_lat = models.DecimalField(decimal_places=6, max_digits=14, default=0.00)
    start_coordinates_lon = models.DecimalField(decimal_places=6, max_digits=14, default=0.00)

    # Date leaving
    date_leaving = models.DateField(auto_now=False, auto_now_add=False)

    # Boolean for if a round trip
    round_trip = models.BooleanField(default=False)

    # Date returning - OPTIONAL
    return_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    # How many spots are available
    spots = models.IntegerField()

    # The user's first (preferred) name
    driver = models.CharField(max_length=25)

    # A description of the ride that can be 1000 letters long
    notes = models.CharField(max_length=1000, blank=True)

    # The price that the user wants to sell the ride at (per spot)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    # If the ride has been archived or not
    archived = models.BooleanField(default=False)

    # If the ride is currently reported (flagged to be reviewed) or not
    reported = models.BooleanField(default=False)

    # VIsible, HiDden, REmoved, or ARchived
    archivedType = ArchivedType.archivedTypeField()

    def __str__(self):
        return self.destination_city

    def __getName__(self):
        return self.username.first_name
