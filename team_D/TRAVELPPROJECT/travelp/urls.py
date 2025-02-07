from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import create_fundraising
 
app_name = 'travelp'
 
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search', views.SearchView.as_view(), name='search'),
    path('search_result', views.SearchResultView.as_view(), name='search_result'),
    path('myprofile', views.MyProfileView.as_view(), name='myprofile'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='user_profile'),
    path('profile/edit/<int:pk>/', views.EditProfileView.as_view(), name='edit_profile'),
    path('post/', views.PostCreateView.as_view(), name='post'),
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
    path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:post_pk>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('post/<int:post_pk>/comment', views.AddCommentView.as_view(), name='add_comment'),
    path('post/<int:post_pk>/comment/<int:comment_id>/delete', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('mypost/', views.mypost, name='mypost'),
    path('myplan/<int:plan_id>/delete/', views.delete_plan, name='delete_plan'),  # プラン削除
    path('create_plan/', views.create_plan, name='create_plan'),
    path('save_plan/', views.save_plan, name='save_plan'),
    path('myplan/', views.myplan, name='myplan'),  # プラン一覧ページ
    path('myplan/<int:plan_id>/', views.plan_detail, name='plan_detail'),  # プラン詳細ページ
    
    # 募金機能
    path('fundraising/', views.fundraising_list, name='fundraising_list'),
    path('fundraising/<int:pk>/', views.fundraising_detail, name='fundraising_detail'),
    path('fundraising/donation-history/', views.donation_history, name='donation_history'),
    path('fundraising/donation-history/<int:pk>/', views.donation_detail, name='donation_detail'),

 
    #市役所
    path('fundraising/create/', create_fundraising, name='create_fundraising'),
    path('fundraising/<int:pk>/delete/', views.fundraising_delete, name='fundraising_delete'),


    # 募金機能
    path('fundraising/<int:pk>/donate/', views.donate, name='donate'),

    # ✅ create_checkout_session の URL を統一
    path('fundraising/<int:pk>/checkout/', views.create_checkout_session, name='create_checkout_session'),
]
 
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)