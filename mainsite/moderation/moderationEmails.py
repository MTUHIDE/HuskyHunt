from django.core.mail import BadHeaderError, send_mail, EmailMessage
from datetime import datetime, timedelta
from catalog.models import CatalogItem
from rideSharing.models import RideItem
from django.contrib.auth.models import User

# Sends an email notification to a user whose item has been removed by moderation.
# Parameters:
#   item: The CatalogItem being removed.
#   reason: A string giving the reason for being removed.
def sendRemoveItemEmail(item, reason):
    user = User.objects.get(username = item.username)

    #The body of the email
    message = (
        'Hello ' + user.first_name + ',\n' +
        'Your item titled ' + item.item_title + ' has been removed by a moderator from our site.' + 
        'The reason for this is "' + reason + '". Any time an item is removed, your future posts are more ' + 
        'likely to be reviewed by our moderation team.\n\nAdditional posts which break our guidelines may result in account suspension.' +
        '\n\nFor more information, contact the HuskyHunt team at huskyhunt-l@mtu.edu\n\n\nThis is an automated message.');

    #The email that this message is sent from
    from_email = 'Admin via HuskyHunt <admin@huskyhunt.com>'
    to_email = user.email

    email = EmailMessage(
        'Item Removed By a Moderator', # subject
        message, #body
        from_email, # from_email
        [to_email],  # to email
        reply_to=['huskyhunt-l@mtu.edu'],  # reply to email
        )
    email.send();

def sendRemoveRideEmail():

# def sendSuspendUserEmail():

# def sendItemMarkedAsAcceptableEmail():

# def sendRideMarkedAsAcceptableEmail():