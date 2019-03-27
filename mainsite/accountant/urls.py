from django.urls import path
from . import views

app_name = 'accountant'
urlpatterns = [
    path('edit/', views.index, name='index'),
    path('catalog/', views.catalogRedirect, name='authsuccess'),
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
]
