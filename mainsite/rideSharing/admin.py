from django.contrib import admin
from .models import RideItem, RideCategory

class RideItemAdmin(admin.ModelAdmin):
    list_display = ('date_added', 'username', 'driver', 'start_city', 'start_state', 'destination_city', 
    	'destination_state', 'date_leaving', 'return_date', 'archived')
    list_filter = ['archived', 'date_added', 'username']

class RideCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['category_name']}),
        ('Date information', {'fields': ['date_added'], 'classes': ['collapse']}),
    ]
    list_display = ('date_added', 'category_name')
    list_filter = ['date_added', 'date_updated']

admin.site.register(RideCategory)
admin.site.register(RideItem, RideItemAdmin)