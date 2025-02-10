from django.urls import path
from .views import (
    SignUpView, SignUpSuccessView, LoginView, logout_view,
    delete_account, password_change_view, password_change_done_view,
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
    
    # パスワード変更
    path('password_change/', password_change_view, name='password_change'),
    path('password_change_done/', password_change_done_view, name='password_change_done'),

    # パスワードリセット関連
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
