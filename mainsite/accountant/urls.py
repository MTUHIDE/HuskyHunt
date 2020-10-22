from django.urls import path
from . import views

#from .views import AccountDetailView

app_name = 'accountant'
urlpatterns = [
    path('edit/', views.edit, name='edit' ),  #AccountDetailView.as_view()
    path('catalog/', views.catalogRedirect, name='authsuccess'),
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('developer/', views.developer, name='developer'),
    path('developer/token/generate', views.developer_generate_token, name='generateToken'),

    # used for deleting an item
    path('<int:pk>/', views.deleteItem, name='deleteItem'),

    # used for deleting a ride
    path('ride/<int:pk>/', views.deleteRide, name='deleteRide'),
]
