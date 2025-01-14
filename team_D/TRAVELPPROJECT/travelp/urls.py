from . import views
from django.urls import path

app_name = 'travelp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('', views.IndexView.as_view(), name='home'),

    path('search', views.SearchView.as_view(), name='search'),

    path('post', views.PostView.as_view(), name='post'),

    path('profile', views.ProfileView.as_view(), name='profile'),

    path('mypost', views.MypostView.as_view(), name='mypost'),

    path('myplan', views.MyplanView.as_view(), name='myplan'),
    
    path('pay', views.PayView.as_view(), name='pay'),


]
