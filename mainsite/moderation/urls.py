from django.urls import path
from . import views

app_name = 'moderation'

#Array that contains string tokens and what to do if the token is found
urlpatterns = [
    #If the next token in the url is...
    #...blank then execute the index methon in views
    path('', views.index, name='index'),
    path('<int:pk>/approve/', views.approve, name='approve'),
    path('<int:pk>/deny/', views.deny, name='deny'),
    path('<int:pk>/ban/', views.ban, name='ban'),
]