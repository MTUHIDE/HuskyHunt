from django.core.mail import BadHeaderError, send_mail, EmailMessage
from datetime import datetime, timedelta
from catalog.models import CatalogItem
from rideSharing.models import RideItem
from django.contrib.auth.models import User
from datetime import datetime

# Sends an email notification to a user whose item has been removed by moderation.
# Parameters:
#   item: The CatalogItem being removed.
#   reason: A string giving the reason for being removed.
def sendRemoveItemEmail(item, reason):
    user = User.objects.get(username = item.username)

    #The body of the email
    message = (
        'Hello ' + user.first_name + ',\n\n' +
        'Your item titled ' + item.item_title + ' has been removed by a moderator from our site.' + 
        'The reason for this is "' + reason + '". Any time an item is removed, your future posts are more ' + 
        'likely to be reviewed by our moderation team.\n\nAdditional posts which break our guidelines may result in account suspension.' +
        '\n\nFor more information, contact the HuskyHunt team at huskyhunt-l@mtu.edu\n\n\nThis is an automated message.');

    #The email that this message is sent from
    from_email = 'Admin via HuskyHunt <admin@huskyhunt.com>'
    to_email = user.email

    email = EmailMessage(
        'Item Removed By Moderator', # subject
        message, #body
        from_email, # from_email
        [to_email],  # to email
        reply_to=['huskyhunt-l@mtu.edu'],  # reply to email
        )
    email.send();

# Sends an email notification to a user whose ride has been removed by moderation.
# Parameters:
#   ride: The RideItem being removed.
#   reason: A string giving the reason for being removed.
def sendRemoveRideEmail(ride, reason):
    user = User.objects.get(username = ride.username)

    #The body of the email
    message = (
        'Hello ' + user.first_name + ',\n\n' +
        'Your ride to ' + ride.destination_city + ' on ' + ride.date_leaving.strftime("%m/%d/%Y") + ' has been removed by a moderator from our site.' + 
        'The reason for this is "' + reason + '". Any time a ride is removed, your future posts are more ' + 
        'likely to be reviewed by our moderation team.\n\nAdditional posts which break our guidelines may result in account suspension.' +
        '\n\nFor more information, contact the HuskyHunt team at huskyhunt-l@mtu.edu\n\n\nThis is an automated message.');

    #The email that this message is sent from
    from_email = 'Admin via HuskyHunt <admin@huskyhunt.com>'
    to_email = user.email

    email = EmailMessage(
        'Ride Removed By Moderator', # subject
        message, #body
        from_email, # from_email
        [to_email],  # to email
        reply_to=['huskyhunt-l@mtu.edu'],  # reply to email
        )
    email.send();

# Sends an email notification to a user who is being suspended
# Parameters:
#   user: The user being suspended
#   type: The type of suspension (seven, thirty, ban)
#   reason: A string giving the reason for suspension
def sendSuspendUserEmail(user, type, reason):
    #The body of the email
    message = ('Hello ' + user.first_name + ',\n\nYour account has been ');

    if (type == "seven"):
    	message += 'suspended for seven days. '
    elif (type == "thirty"):
    	message += 'suspended for thirty days. '
    else:
    	message += 'banned. '

    message += (
        'The reason for this is "' + reason + '".' + 
        '\n\nFor more information, contact the HuskyHunt team at huskyhunt-l@mtu.edu\n\n\nThis is an automated message.');

    #The email that this message is sent from
    from_email = 'Admin via HuskyHunt <admin@huskyhunt.com>'
    to_email = user.email

    email = EmailMessage(
        'Account Suspension', # subject
        message, #body
        from_email, # from_email
        [to_email],  # to email
        reply_to=['huskyhunt-l@mtu.edu'],  # reply to email
        )
    email.send();