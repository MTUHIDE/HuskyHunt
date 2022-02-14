from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from social_core.pipeline.partial import partial
from catalog.views import isUserNotBanned
from django.contrib import messages
from django.contrib.auth import logout


# Create your views here.
def index(request):
    template = 'landing/index.html'
    context = {}
    if request.user.is_authenticated:
        if not isUserNotBanned(request.user):
            messages.warning(request, 'Your account is currently suspended.')
            logout(request)
            return HttpResponseRedirect('/')

        return HttpResponseRedirect('/welcome/')

    return render(request, template, context)


def signup(request):
    template = 'landing/signup.html'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, template, context)


def passwordReset(email, from_email):
    template = 'registration/password_reset_email.html'
    form = PasswordResetForm({'email': email})
    return form.save(from_email=from_email, email_template_name=template)


def welcome(request):
    template = 'landing/welcome.html'
    context = {}

    return render(request, template, context)
