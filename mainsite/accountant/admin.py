from django.contrib import admin
from accountant.models import user_profile
from datetime import datetime, timedelta
import pytz
from django.core.mail import BadHeaderError, send_mail, EmailMessage


@admin.register(user_profile)
class user_profileAdmin(admin.ModelAdmin):
	name = 'test'
	actions = ['timeout_user_seven', ]

	def timeout_user_seven(self, request, queryset):
		# Reset points, timeout user(s) for 7 days
		queryset.update(points=0)
		banned_untilDateTime = (datetime.now() + timedelta(days=7)).astimezone(pytz.timezone('UTC'))
		queryset.update(banned_until = banned_untilDateTime)

		# Send emails
		for user in queryset:
			#The body of the email
			message = ('Your account on HuskyHunt has been suspended for seven days.\n')

			#The email that this message is sent from
			from_email = 'Admin via HuskyHunt <admin@huskyhunt.com>'
			to_email = user.user.email

			email = EmailMessage(
		    	'Account Suspended', # subject
		        message, #body
		        from_email, # from_email
		        [to_email],  # to email
		        reply_to=[],  # reply to email
		        )
			email.send();


	timeout_user_seven.short_description = "Timeout User 7 days"

