from django.contrib import admin
from .models import RideCategory
from moderation.moderationActions import *


class RideCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['category_name']}),
        ('Date information', {'fields': ['date_added'], 'classes': ['collapse']}),
    ]
    list_display = ('date_added', 'category_name')
    list_filter = ['date_added', 'date_updated']


class RideItemAdmin(admin.ModelAdmin):
    list_display = (
        'reported', 'archived', 'archivedType', 'date_added', 'username', 'driver', 'start_city', 'start_state',
        'destination_city',
        'destination_state', 'date_leaving', 'return_date')
    list_filter = ['reported', 'archived', 'date_added', 'username']
    # search_fields ?
    actions = ['remove_post', 'allow_post', 'ignore_post', 'delete_post']

    def remove_post(self, request, queryset):
        remove_ride(queryset, '[ADMIN MANUAL REMOVAL]')

    remove_post.short_description = "Remove offending posts"

    def allow_post(self, request, queryset):
        make_ride_public(queryset)

    allow_post.short_description = "Unarchive: mark acceptable"

    def ignore_post(self, request, queryset):
        ignore_report(queryset)

    ignore_post.short_description = "Ignore report (don't use this, unarchive instead)"

    def get_actions(self, request):
        # https://stackoverflow.com/questions/34152261/remove-the-default-delete-action-in-django-admin
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(RideCategory)
admin.site.register(RideItem, RideItemAdmin)
