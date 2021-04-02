from django.contrib import admin
from .models import CatalogItem, Category
from accountant.models import user_profile
from profanity_check.models import ArchivedType
from moderation.moderationActions import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['category_name']}),
        ('Date information', {'fields': ['date_added'], 'classes': ['collapse']}),
    ]
    list_display = ('date_added', 'category_name')
    list_filter = ['date_added', 'date_updated']
    
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ('reported', 'archived', 'archivedType', 'pk', 'date_added', 'username', 'item_price', 'item_title', 'item_description')
    list_filter = ['reported', 'archived', 'category', 'date_added', 'username']
    search_fields = ['item_title', 'item_description']
    actions = ['remove_post', 'allow_post', 'ignore_post', 'delete_post']

    def remove_post(self, request, queryset):
        remove_item(queryset, '[ADMIN MANUAL REMOVAL]')

    remove_post.short_description = "Remove offending posts (reported=True, archived=True, type=Removed)"

    def delete_post(self, request, queryset):
        queryset.update(archived=True)
        queryset.update(archivedType=ArchivedType.Types.ARCHIVED)
        # Decrement number of points by three
        for item in queryset:
            profile = user_profile.objects.get(user = item.username)
            profile.points = profile.points - 3
            profile.save()
    delete_post.short_description = "Delete posts (archived=True, type=archived)"

    def allow_post(self, request, queryset):
        make_item_public(queryset)
    allow_post.short_description = "Make public (reported=False, archived=False, type=visble)"

    def ignore_post(self, request, queryset):
        ignore_report(queryset)
    ignore_post.short_description = "Ignore report (reported=False)"

    def get_actions(self, request):
        #https://stackoverflow.com/questions/34152261/remove-the-default-delete-action-in-django-admin
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(Category)
admin.site.register(CatalogItem, CatalogItemAdmin)
