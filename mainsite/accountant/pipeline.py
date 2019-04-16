from django.http import HttpResponseRedirect

def verify_scope(backend, user, response, *args, **kwargs):
    if not user.email.endswith('@mtu.edu'):
        return HttpResponseRedirect('/')