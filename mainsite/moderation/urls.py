from django.urls import path
from . import views

app_name = 'moderation'

# Array that contains string tokens and what to do if the token is found
urlpatterns = [
    # If the next token in the url is...
    # ...blank then execute the index methon in views
    path('', views.index, name='index'),
    path('item/<int:pk>/approve/', views.approve_item, name='approve_item'),
    path('item/<int:pk>/deny/', views.deny_item, name='deny_item'),
    path('ride/<int:pk>/approve/', views.approve_ride, name='approve_ride'),
    path('ride/<int:pk>/deny/', views.deny_ride, name='deny_ride'),
    path('<int:pk>/ban/', views.ban, name='ban'),
]
