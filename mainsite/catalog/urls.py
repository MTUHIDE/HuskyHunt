from django.urls import path
from . import views

app_name = 'catalog'

#Array that contains string tokens and what to do if the token is found
urlpatterns = [
    #If the next token in the url is...

    #...an integer then execute the detail method in views
    path('<int:pk>/', views.detail, name='detail'),

    #...blank then execute the index methon in views
    path('', views.index, name='index'),

    #...search/ then execute the search method in views
  	path('search/', views.search, name='search'),

    #...filter/a category/ then execute the filter method in views
  	path('filter/', views.filter, name='filter'),

    #...an integer followed by /email then execute the email method in views
    path('<int:pk>/email/', views.email, name='email'),
]
