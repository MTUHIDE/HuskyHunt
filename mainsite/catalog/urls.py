from django.urls import path
#from django.urls import re_path
from . import views

app_name = 'catalog'
urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('', views.index, name='index'),
  	path('search/', views.search, name='search'),
  	path('filter/<category>/', views.filter, name='filter'),
]

#path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#path('<int:question_id>/results/', views.results, name='results'),
#path('<int:question_id>/vote/', views.vote, name='vote'),
