from django.urls import path
from . import views

from .views import AccountDetailView

app_name = 'accountant'
urlpatterns = [
    path('edit/', AccountDetailView.as_view(), name='edit' ),
    path('catalog/', views.catalogRedirect, name='authsuccess'),
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),

    # used for deleting an item
    path('<int:pk>/', views.deleteItem, name='deleteItem'),
]
