from django.http import HttpResponseRedirect
from django.contrib import messages

def verify_scope(request, backend, user, response, *args, **kwargs):
    if not user.email.endswith('@mtu.edu'):
        messages.warning(request, 'Please log in with your MTU email.')
        return HttpResponseRedirect('/')