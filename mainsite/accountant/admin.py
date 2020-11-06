from django.contrib import admin
from accountant.models import user_profile
from datetime import datetime, timedelta
import pytz


@admin.register(user_profile)
class user_profileAdmin(admin.ModelAdmin):
	name = 'test'
	actions = ['timeout_user_seven', ]

	def timeout_user_seven(self, request, queryset):
		# Reset points, timeout user for 7 days
		queryset.update(points=0)
		banned_untilDateTime = (datetime.now() + timedelta(days=7)).astimezone(pytz.timezone('UTC'))
		queryset.update(banned_until = banned_untilDateTime)

	timeout_user_seven.short_description = "Timeout User 7 days"

