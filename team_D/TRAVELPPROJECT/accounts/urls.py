from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

# アプリケーション名
app_name = "accounts"

urlpatterns = [
    # サインアップ:signup
    path(
        "signup",
        views.SignUpView.as_view(),
        name="signup",
    ),

    # サインアップ完了:signup_done
    path(
        "signup_done",
        TemplateView.as_view(template_name="accounts/signup_done.html"),
        name="signup_done",
    ),

    # ログイン:login
    path(
        "login", views.LoginView.as_view(), name="login"
    ),

    # パスワードリセット:password_reset
    path(
        "password_reset",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),

    # パスワードリセット送信完了:password_reset_done
    path(
        "password_reset_done",
        TemplateView.as_view(template_name="accounts/password_reset_done.html"),
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

    # パスワード変更:password_change
    path(
        "password_change",
        views.PasswordChangeView.as_view(template_name="accounts/password_change.html"),
        name="password_change",
    ),

    # パスワード変更完了:password_change_done
    path(
        "password_change_done",
        TemplateView.as_view(template_name="accounts/password_change_done.html"),
        name="password_change_done",
    ),

    # ログアウト:logout
    path(
        "logout",
        LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
]
