"""mainsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url, include

urlpatterns = [
    path('accountant/', include('accountant.urls', namespace='accountant')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('ridesharing/', include('rideSharing.urls', namespace='rideSharing')),
    path('polls/', include('polls.urls', namespace='polls')),
    path('selling/', include('selling.urls', namespace='selling')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('landing.urls', namespace='landing')),
    url(r'^auth/', include('social_django.urls', namespace='social')),  # <- Here
    path('auth/complete/google-oauth2/', include('accountant.urls', namespace='authsuccess')),
]

from .import settings
from django.contrib.staticfiles.urls import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
