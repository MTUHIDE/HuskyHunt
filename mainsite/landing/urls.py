from django.urls import path, include
from . import views

app_name = 'landing'
urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),
]
#urlpatterns = [
#    path('auth/', include('django.contrib.auth.urls')),
#    path('', views.IndexView.as_view(), name='index'),
#    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#    path('<int:question_id>/results/', views.results, name='results'),
#    path('<int:question_id>/vote/', views.vote, name='vote'),
#    path('', views.index, name='index'),
#]
