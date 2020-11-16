from django.urls import path
from . import views

app_name = 'catalog'

#Array that contains string tokens and what to do if the token is found
urlpatterns = [
    #If the next token in the url is...

    #...an integer then execute the detail method in views
    path('<int:pk>/', views.detail, name='detail'),

    #...an integer then execute the update method in views
    path('<int:pk>/update/', views.update, name='update'),

    #...blank then execute the index methon in views
    path('', views.index, name='index'),

    #...filter/a category/ then execute the filter method in views
  	path('filter/', views.filter, name='filter'),

    #...an integer followed by /email then execute the email method in views
    path('<int:pk>/email/', views.email, name='email'),

    #...an integer followed by /email then execute the email method in views
    path('<int:pk>/report/', views.report, name='report'),
]
