from django.contrib import admin
from .models import RideItem

class RideItemAdmin(admin.ModelAdmin):
    list_display = ('date_added', 'username', 'price', 'start_city', 'start_state', 'start_zipcode', 'destination_city', 
    	'destination_state', 'destination_zipcode', 'date_leaving', 'round_trip', 'return_date', 'spots', 'driver', 'notes')
    list_filter = ['date_added', 'username']

admin.site.register(RideItem, RideItemAdmin)