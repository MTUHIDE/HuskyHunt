from django.contrib import admin
from accountant.models import user_profile
from datetime import datetime, timedelta
import pytz
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from catalog.models import CatalogItem

def archiveAllUserPosts(user):
	items = CatalogItem.objects.filter(archived='False', username=user.user)
	for item in items:
		item.archived=True
		item.save()

@admin.register(user_profile)
class user_profileAdmin(admin.ModelAdmin):
	name = 'test'
	actions = ['timeout_user_seven', 'timeout_user_thirty', 'ban_user']

	def timeout_user_seven(self, request, queryset):
		# Reset points, timeout user(s) for 7 days
		queryset.update(points=0)
		banned_untilDateTime = (datetime.now() + timedelta(days=7)).astimezone(pytz.timezone('UTC'))
		queryset.update(banned_until = banned_untilDateTime)

		# Send emails
		for user in queryset:
			archiveAllUserPosts(user)

			#The body of the email
			message = ('Your account on HuskyHunt has been suspended for seven days.\n\n\nThis is an automated message.')

			#The email that this message is sent from
			from_email = 'Admin via HuskyHunt <admin@huskyhunt.com>'
			to_email = user.user.email

			email = EmailMessage(
		    	'Account Suspended', # subject
		        message, #body
		        from_email, # from_email
		        [to_email],  # to email
		        reply_to=[to_email],  # reply to email
		        )
			email.send();


	def timeout_user_thirty(self, request, queryset):
		# Reset points, timeout user(s) for 30 days
		queryset.update(points=0)
		banned_untilDateTime = (datetime.now() + timedelta(days=30)).astimezone(pytz.timezone('UTC'))
		queryset.update(banned_until = banned_untilDateTime)

		# Send emails
		for user in queryset:
			archiveAllUserPosts(user)

			#The body of the email
			message = ('Your account on HuskyHunt has been suspended for thirty days.\n\n\nThis is an automated message.')

			#The email that this message is sent from
			from_email = 'Admin via HuskyHunt <admin@huskyhunt.com>'
			to_email = user.user.email

			email = EmailMessage(
		    	'Account Suspended', # subject
		        message, #body
		        from_email, # from_email
		        [to_email],  # to email
		        reply_to=[to_email],  # reply to email
		        )
			email.send();

	def ban_user(self, request, queryset):
		# Reset points, ban user(s) for 1000 days
		queryset.update(points=0)
		banned_untilDateTime = (datetime.now() + timedelta(days=1000)).astimezone(pytz.timezone('UTC'))
		queryset.update(banned_until = banned_untilDateTime)

		# Send emails
		for user in queryset:
			archiveAllUserPosts(user)

			#The body of the email
			message = ('Your account on HuskyHunt has been banned.\n\n\nThis is an automated message.')

			#The email that this message is sent from
			from_email = 'Admin via HuskyHunt <admin@huskyhunt.com>'
			to_email = user.user.email

			email = EmailMessage(
		    	'Account Banned', # subject
		        message, #body
		        from_email, # from_email
		        [to_email],  # to email
		        reply_to=[to_email],  # reply to email
		        )
			email.send();

	timeout_user_seven.short_description = "Timeout 7 Days"
	timeout_user_thirty.short_description = "Timeout 30 Days"
	ban_user.short_description = "Ban User"

	def get_actions(self, request):
		#https://stackoverflow.com/questions/34152261/remove-the-default-delete-action-in-django-admin
		actions = super().get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions;

