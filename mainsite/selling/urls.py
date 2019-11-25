from django.urls import path
from . import views

app_name = 'selling'
urlpatterns = [
    path('', views.catalog_item_form, name='index'),
    path('ctlg', views.catalog_item_form, name='catalog_item_create'),
    path('ride', views.RideCreate.as_view(), name='ride_create')
]


#    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#    path('<int:question_id>/results/', views.results, name='results'),
#    path('<int:question_id>/vote/', views.vote, name='vote'),
#    path('', views.index, name='index'),
