# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
# from .models import Account

# # Register your models here.
# class AccountInline(admin.StackedInline):
#     model = Account

# class AccountAdmin(UserAdmin):
#     inlines = (AccountInline,)
# #     list_display = ('username', 'email', 'last_login')
# #     fieldsets = [
# #         (None,     {'fields': ['username', 'first_name', 'last_name', 'email', 'street_address', 'city', 'zipcode', 'common_destination_zipcode', 'picture', 'bio']}),
# #         ('Permissions',  {'fields': ['password', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined']}),
# #     ]
# #     search_fields = ['username', 'email']

# admin.site.unregister(User)
# admin.site.register(User, AccountAdmin)
