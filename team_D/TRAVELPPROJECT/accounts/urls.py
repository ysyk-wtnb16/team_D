from django.urls import path
from . import views
from .views import (
    TemplateView,SignUpView, SignUpSuccessView, LoginView, logout_view,
    delete_account, 
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

app_name = 'accounts'

urlpatterns = [
    # サインアップ
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/success/', SignUpSuccessView.as_view(), name='signup_success'),
    
    # ログイン
    path('login/', LoginView.as_view(), name='login'),
    
    # ログアウト
    path('logout/', logout_view, name='logout'),
    
    # アカウント削除
    path('delete_account/', delete_account, name='delete_account'),
    
 # パスワードリセット:password_reset
    path(
        "password_reset",views.PasswordResetView.as_view(),
        name="password_reset",
    ),
 
    # パスワードリセット送信完了:password_reset_done
    path(
        "password_reset_done",TemplateView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
 
    # パスワードリセットフォーム:password_reset_form
    path(
        "password_reset_form/<uidb64>/<token>",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_form",
    ),
 
    # パスワードリセット完了:password_reset_form_done
    path(
        "password_reset_form_done",
        TemplateView.as_view(template_name="accounts/password_reset_form_done.html"),
        name="password_reset_form_done",
    ),
]
