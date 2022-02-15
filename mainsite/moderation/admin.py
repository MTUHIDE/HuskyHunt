from django.contrib import admin
from .models import ItemModerationActions, RideModerationActions, InitialContactLog


# Register your models here.

class ItemModerationActionsAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'action_type', 'reason', 'date_action')
    list_filter = ['action_type']


class RideModerationActionsAdmin(admin.ModelAdmin):
    list_display = ('ride_id', 'action_type', 'reason', 'date_action')
    list_filter = ['action_type']


class InitialContactLogAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'date_sent', 'message')
    list_filter = ['sender', 'receiver']


admin.site.register(ItemModerationActions)
admin.site.register(RideModerationActions)
admin.site.register(InitialContactLog)
