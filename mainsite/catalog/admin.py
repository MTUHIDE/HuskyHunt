from django.contrib import admin
from .models import CatalogItem, Category, SubCategory

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
    list_display = ('date_added', 'username', 'item_price', 'item_title', 'item_description')
    list_filter = ['category', 'date_added', 'username']
    search_fields = ['item_title', 'item_description']

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(CatalogItem, CatalogItemAdmin)
