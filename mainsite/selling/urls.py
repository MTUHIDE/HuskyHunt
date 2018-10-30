from django.urls import path
from . import views

app_name = 'selling'
urlpatterns = [
    path('', views.index, name='index'),
#    path('', views.SellingListView.as_view(), name='index'),
]
#    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#    path('<int:question_id>/results/', views.results, name='results'),
#    path('<int:question_id>/vote/', views.vote, name='vote'),
#    path('', views.index, name='index'),

