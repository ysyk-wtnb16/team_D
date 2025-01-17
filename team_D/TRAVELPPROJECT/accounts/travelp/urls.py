from . import views
from django.urls import path

app_name = 'travelp'

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),

    path('home', views.IndexView.as_view(), name='home'),

    path('search', views.SearchView.as_view(), name='search'),

    path('post', views.PostView.as_view(), name='post'),

    path('profile', views.ProfileView.as_view(), name='profile'),

    path('mypost', views.MypostView.as_view(), name='mypost'),

    path('myplan', views.MyplanView.as_view(), name='myplan'),
    
    path('pay', views.PayView.as_view(), name='pay'),

    path('s_home', views.S_homeView.as_view(), name='s_home'),

    path('s_sinsei', views.S_sinseiView.as_view(), name='s_sinsei'),

    path('s_page', views.S_pageView.as_view(), name='s_page'),

    path('s_post', views.S_postView.as_view(), name='s_post'),

    path('s_history', views.S_historyView.as_view(), name='s_history'),




]
