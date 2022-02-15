from django.contrib import admin
from accountant.models import user_profile
from datetime import datetime, timedelta
import pytz
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from catalog.models import CatalogItem
from moderation.moderationActions import *


def archiveAllUserPosts(user):
    items = CatalogItem.objects.filter(archived='False', username=user.user)
    for item in items:
        item.archived = True
        item.save()


@admin.register(user_profile)
class user_profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'banned_until', 'digest', 'lastDigest')

    name = 'test'
    actions = ['timeout_user_seven', 'timeout_user_thirty', 'ban_user']

    def timeout_user_seven(self, request, queryset):
        suspend_user(queryset, '[ADMIN MANUAL SUSPENSION]', 7)

    def timeout_user_thirty(self, request, queryset):
        suspend_user(queryset, '[ADMIN MANUAL SUSPENSION]', 30)

    def ban_user(self, request, queryset):
        suspend_user(queryset, '[ADMIN MANUAL SUSPENSION]', 1000)

    timeout_user_seven.short_description = "Timeout 7 Days"
    timeout_user_thirty.short_description = "Timeout 30 Days"
    ban_user.short_description = "Ban User"

    def get_actions(self, request):
        # https://stackoverflow.com/questions/34152261/remove-the-default-delete-action-in-django-admin
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
