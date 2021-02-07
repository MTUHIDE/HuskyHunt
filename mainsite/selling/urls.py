from django.urls import path, re_path
from django.conf import settings
from . import views

app_name = 'selling'
if not settings.DISABLE_SELLING:
	urlpatterns = [
	    path('', views.index, name='index')
	]
else:
  urlpatterns = [
    path('', views.disabled, name="index"),
    re_path(r'^.*/$', views.disabled, name='index'),
  ]