from django.urls import path
from . import views

app_name = 'accountant'
urlpatterns = [
    path('edit/', views.index, name='index'),
    path('', views.index, name='index'),
]
