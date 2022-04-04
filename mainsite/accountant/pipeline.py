from django.http import HttpResponseRedirect
from django.contrib import messages


def verify_scope(request, backend, user, response, *args, **kwargs):
    if not user.email.endswith('@mtu.edu'):
        messages.warning(request, 'Please log in with your MTU email.')
        user.delete()  # Delete the user since we don't need to keep track of users without an mtu email
        return HttpResponseRedirect('/')


def update_user_social_data(strategy, *args, **kwargs):
    # There used to be code here that would automatically sync profile picture data
    # With what was set on google, but didn't seem to work
    pass
