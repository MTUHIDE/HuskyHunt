from django.contrib import admin
from .models import RideItem, RideCategory

class RideItemAdmin(admin.ModelAdmin):
    list_display = ('date_added', 'username', 'price', 'start_city', 'start_state', 'start_zipcode', 'destination_city', 
    	'destination_state', 'destination_zipcode', 'date_leaving', 'round_trip', 'return_date', 'spots', 'driver', 'notes')
    list_filter = ['date_added', 'username']

class RideCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['category_name']}),
        ('Date information', {'fields': ['date_added'], 'classes': ['collapse']}),
    ]
    list_display = ('date_added', 'category_name')
    list_filter = ['date_added', 'date_updated']

admin.site.register(RideCategory)
admin.site.register(RideItem, RideItemAdmin)