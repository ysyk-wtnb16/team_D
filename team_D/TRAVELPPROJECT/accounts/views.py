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


def password_change_view(request):
   if request.method == "POST":
       username = request.POST.get('username')
       new_password = request.POST.get('new_password')
       try:
           user = User.objects.get(username=username)  # ユーザーを取得
           user.set_password(new_password)  # 新しいパスワードを設定
           user.save()
           messages.success(request, "パスワードが変更されました！")
           return redirect('password_change_done')  # 完了ページへリダイレクト
       except User.DoesNotExist:
           messages.error(request, "そのユーザー名は存在しません。")
   return render(request, 'password_change.html')  # パスワード変更フォームを描画
def password_change_done_view(request):
   return render(request, 'password_change_done.html')  # 完了メッセージを表示
from django.contrib.auth import get_user_model

from django.contrib import messages

from django.shortcuts import render, redirect

# 現在のユーザーモデルを取得

# カスタムユーザーのモデルを取得
User = get_user_model()
def password_change_view(request):
   if request.method == 'POST':
       username = request.POST.get('username')
       new_password = request.POST.get('new_password')
       if len(new_password) < 8:  # パスワードが8文字以下の場合
           messages.error(request, "パスワードは8文字以上である必要があります。")
           return redirect('accounts:password_change')
       try:
           user = User.objects.get(username=username)
           if not user:  #ユーザーが見つからない場合の処理
               messages.error(request, "ユーザーが見つかりません。")
               return redirect('accounts:password_change')
           user.set_password(new_password)
           user.save()
           messages.success(request, "パスワードが変更されました！")
           return redirect('accounts:password_change_done')
       except User.DoesNotExist:
           messages.error(request, "そのユーザー名は存在しません。")
           return redirect('travelp:password_change')
   return render(request, 'password_change.html')


def password_change_done_view(request):
    return render(request, 'password_change_done.html')


class PasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
# パスワードリセット完了ビュー
class PasswordResetDoneView(TemplateView):
    template_name = 'password_reset_done.html'

# パスワードリセット確認（メール内のリンクをクリック後）
class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('travelp:password_reset_complete')

# パスワードリセット完了後のビュー
class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
