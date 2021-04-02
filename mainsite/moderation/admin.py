from django.contrib import admin
from .models import ItemModerationActions, RideModerationActions

# Register your models here.

class ItemModerationActionsAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'action_type', 'reason', 'date_action')
    list_filter = ['action_type']

class RideModerationActionsAdmin(admin.ModelAdmin):
    list_display = ('ride_id', 'action_type', 'reason', 'date_action')
    list_filter = ['action_type']

admin.site.register(ItemModerationActions)
admin.site.register(RideModerationActions)