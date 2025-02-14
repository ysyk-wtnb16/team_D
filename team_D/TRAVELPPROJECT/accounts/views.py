from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import CustomUserCreationForm, LoginForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages



class SignUpView(CreateView):
    '''サインアップページのビュー
    
    '''
    # forms.pyで定義したフォームのクラス
    form_class = CustomUserCreationForm
    # レンダリングするテンプレート
    template_name = "signup.html"
    # サインアップ完了後のリダイレクト先のURLパターン
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        '''CreateViewクラスのform_valid()をオーバーライド
        
        フォームのバリデーションを通過したときに呼ばれる
        フォームデータの登録を行う
        
        parameters:
          form(django.forms.Form):
            form_classに格納されているCustomUserCreationFormオブジェクト
        Return:
          HttpResponseRedirectオブジェクト:
            スーパークラスのform_valid()の戻り値を返すことで、
            success_urlで設定されているURLにリダイレクトさせる
        '''
        # formオブジェクトのフィールドの値をデータベースに保存
        user = form.save()
        self.object = user
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)

class SignUpSuccessView(TemplateView):
    '''サインアップ成功ページのビュー
    
    '''
    # レンダリングするテンプレート
    template_name = "signup_success.html"

# ログインビュー
class LoginView(AuthLoginView):
    form_class = LoginForm
    template_name = "login.html"

    # 認証後にリダイレクトするURLを取得するメソッド
    def get_success_url(self):
        return reverse_lazy("travelp:index")
    
def logout_view(request):
    logout(request)
    messages.success(request, "ログアウトしました。")
    return redirect('/')  # トップページのURLパターン名にリダイレクト


@login_required
def delete_account(request):
    if request.method == 'POST':  # POSTリクエストの場合のみ退会処理を行う
        user = request.user
        user.delete()  # ユーザーを削除

        logout(request)  # ログアウト処理
        messages.success(request, 'アカウントが削除されました。')
        return redirect('/')  # 退会後、ホームページにリダイレクト

    return render(request, 'delete_account.html')  # GETリクエスト時は確認ページを表示





from django.contrib.auth.views import PasswordResetView as AuthPasswordResetView
from .forms import PasswordResetForm
 
 
# パスワードリセットビュー
class PasswordResetView(AuthPasswordResetView):
    template_name = "accounts/password_reset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("accounts:password_reset_done")
    # メールのテンプレート
    email_template_name = "accounts/password_reset_email.html"
 
 
from django.contrib.auth.views import (
    PasswordResetConfirmView as AuthPasswordResetConfirmView,
)
from django.contrib.auth.forms import SetPasswordForm as AuthSetPasswordForm
 
 
# パスワードリセット新パスワード入力ビュー
class PasswordResetConfirmView(AuthPasswordResetConfirmView):
    # 内部クラス...このクラス(PasswordResetConfimView)だけが使えるクラス
    class SetPasswordForm(AuthSetPasswordForm):
        error_messages = {"password_mismatch": "パスワードが一致しません"}
 
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["new_password1"].widget.attrs["class"] = "form-control ms-5"
            self.fields["new_password2"].widget.attrs["class"] = "form-control ms-5"
 
    template_name = "accounts/password_reset_form.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("accounts:password_reset_form_done")