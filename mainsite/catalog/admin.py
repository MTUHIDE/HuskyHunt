from django.contrib import admin
from .models import CatalogItem, Category, SubCategory
from accountant.models import user_profile


# Register your models here.
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['category_name']}),
        ('Date information', {'fields': ['date_added'], 'classes': ['collapse']}),
    ]
    list_display = ('date_added', 'category_name')
    list_filter = ['date_added', 'date_updated']
    inlines = [SubCategoryInline]

class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ('reported', 'pk', 'date_added', 'username', 'item_price', 'item_title', 'item_description', 'archived')
    list_filter = ['reported', 'archived', 'category', 'date_added', 'username']
    search_fields = ['item_title', 'item_description']
    actions = ['remove_post', ]

    def remove_post(self, request, queryset):
        queryset.update(reported=True)
        queryset.update(archived=True)

        # Decrement number of points by three
        for item in queryset:
            profile = user_profile.objects.get(user = item.username)
            profile.points = profile.points - 3
            profile.save()

    remove_post.short_description = "Remove offending posts"




admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(CatalogItem, CatalogItemAdmin)
