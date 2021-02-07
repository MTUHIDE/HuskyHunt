from django.urls import path, re_path
from django.conf import settings
from . import views

app_name = 'rideSharing'

#Array that contains string tokens and what to do if the token is found
if not settings.DISABLE_RIDESHARING:
  urlpatterns = [
      #If the next token in the url is...
      #...blank then execute the index methon in views
      path('', views.index, name='index'),

      # index to show the modal
      path('<int:pk>/', views.ride, name="ride"),

      #...search/ then execute the search method in views
    	path('search/', views.search, name='search'),

    	#...filter/a category/ then execute the filter method in views
    	path('filter/', views.filter, name='filter'),

    	#...an integer followed by /email then execute the email method in views
      path('<int:pk>/email/', views.email, name='email'),

      #...an integer followed by /email then execute the email method in views
      path('<int:pk>/report/', views.report, name='report'),
  ]
else:
  urlpatterns = [
    path('', views.disabled, name="index"),
    re_path(r'^.*/$', views.disabled, name='index'),
  ]