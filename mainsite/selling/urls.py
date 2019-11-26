from django.urls import path
from . import views

app_name = 'selling'
urlpatterns = [
    path('', views.index, name='index')
]
