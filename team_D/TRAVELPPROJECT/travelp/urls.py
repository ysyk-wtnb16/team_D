from . import views
from django.urls import path

app_name = 'travelp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),

    path('index', views.IndexView.as_view(), name='index'),

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

 # サインアップとログインページの（追加した）
    path('login/',views.LoginView.as_view(),name='login'),

    path('signup/', views.SignupView.as_view(), name='signup'),

    path('signup/done/', views.SignupDoneView.as_view(), name='signup_done'),  # signup_doneページ

    path('logout/', views.LogoutView.as_view(), name='logout'),  # クラスベースのログアウトURL

    path('s_base/', views.SBaseView.as_view(), name='s_base'),  # スタッフ用ページ



    path('password_change/', views.password_change_view, name='password_change'),
   path('password_change/done/', views.password_change_done_view, name='password_change_done'),

]
