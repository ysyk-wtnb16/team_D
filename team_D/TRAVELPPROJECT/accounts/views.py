from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as AuthLoginView
from .forms import CustomUserCreationForm, LoginForm
from django.urls import reverse_lazy



# 会員登録ビュー
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:signup_done")
    def form_valid(self, form):
        # 会員を登録
        user = form.save()
        self.object = user

# ログインビュー
class LoginView(AuthLoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    
    # 認証後にリダイレクトするURLを取得するメソッド
    def get_success_url(self):
        return reverse_lazy("main:index")


from django.contrib.auth.views import PasswordResetView as AuthPasswordResetView
from .forms import PasswordResetForm

# パスワードリセットビュー
class PasswordResetView(AuthPasswordResetView):
    template_name = "accounts/password_reset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("accounts:password_reset_done")
    # メールのテンプレート
    email_template_name = "accounts/password_reset_email.html"


from django.contrib.auth.views import PasswordResetConfirmView as AuthPasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm as AuthSetPasswordForm

# パスワードリセット新パスワード入力ビュー
class PasswordResetConfirmView(AuthPasswordResetConfirmView):
    # 内部クラス...このクラス(PasswordResetConfimView)だけが使えるクラス
    class SetPasswordForm(AuthSetPasswordForm):
        error_messages = {
            "password_mismatch": "パスワードが一致しません"
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["new_password1"].widget.attrs["class"] = "form-control ms-5"
            self.fields["new_password2"].widget.attrs["class"] = "form-control ms-5"

    template_name = "accounts/password_reset_form.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy(
        "accounts:password_reset_form_done")


from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm

# パスワード変更ビュー
class PasswordChangeView(AuthPasswordChangeView):
    class PasswordChangeForm(AuthPasswordChangeForm):
        error_messages = {
                "password_incorrect": "旧パスワードが間違っています",
                "password_mismatch":"新パスワードが一致しません"
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields["old_password"].widget.attrs["class"] = "form-control ms-5"
            self.fields["new_password1"].widget.attrs["class"] = "form-control ms-5"
            self.fields["new_password2"].widget.attrs["class"] = "form-control ms-5"

    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")
    form_class = PasswordChangeForm
