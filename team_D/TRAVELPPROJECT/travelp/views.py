from django.shortcuts import render, redirect

from django.views.generic.base import TemplateView

from django.urls import reverse_lazy

from django.views.generic.edit import CreateView

from .forms import SignupForm

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login

from django.contrib import messages

from django.contrib.auth import login as auth_login

from django.contrib.auth import logout as auth_logout


class IndexView(TemplateView):

    template_name = 'index.html'

class SearchView(TemplateView):

    template_name = 'search.html'

class PostView(TemplateView):

    template_name = 'post.html'

class ProfileView(TemplateView):

    template_name = 'profile.html'

class MypostView(TemplateView):

    template_name = 'mypost.html'

class MyplanView(TemplateView):

    template_name = 'myplan.html'

class PayView(TemplateView):

    template_name = 'pay.html'

class S_homeView(TemplateView):

    template_name = 's_home.html'

class S_sinseiView(TemplateView):

    template_name = 's_sinsei.html'

class S_pageView(TemplateView):

    template_name = 's_page.html'

class S_postView(TemplateView):

    template_name = 's_post.html'

class S_historyView(TemplateView):

    template_name = 's_history.html'

# サインアップビュー(追加した)

class SignupView(CreateView):

    form_class = SignupForm

    template_name = 'signup.html'

    success_url = reverse_lazy('travelp:signup_done')  # 完了ページへリダイレクト

# ログインビュー（追加した↓）
class LoginView(TemplateView):
    template_name = 'login.html'
    def post(self, request, *args, **kwargs):
       username = request.POST.get('user-id')
       password = request.POST.get('password')

       user = authenticate(request, username=username, password=password)
       if user is not None:
           
           login(request, user)
           # ユーザーのメールアドレスを確認
           if user.email.endswith('@travelp.com'):
               # メールアドレスが@example.comであればスタッフページへリダイレクト
               return redirect('travelp:s_base')  # スタッフ用ページ
           else:
               # それ以外のユーザーはインデックスページにリダイレクト
               return redirect('travelp:index')
       else:
           messages.error(request, "ユーザーIDまたはパスワードが間違っています。")
           return render(request, self.template_name)



class LogoutView(TemplateView):
   def get(self, request, *args, **kwargs):
       auth_logout(request)
       
       return redirect('travelp:signup')

# signup_doneページ

class SignupDoneView(TemplateView):

    template_name = 'signup_done.html'

    # GETリクエストを処理

    def get(self, request, *args, **kwargs):

        # 必要なら追加の処理を行うことができます

        return super().get(request, *args, **kwargs) 
    
class SignupView(CreateView):

    form_class = SignupForm

    template_name = 'signup.html'

    success_url = reverse_lazy('travelp:signup_done')  # 完了ページへリダイレクト

class SBaseView(TemplateView):
   template_name = 's_base.html'  # スタッフ用ページ 