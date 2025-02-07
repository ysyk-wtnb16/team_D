# UserCreationFormクラスをインポート
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import CheckboxSelectMultiple, EmailInput
# models.pyで定義したカスタムUserモデルをインポート
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    '''UserCreationFormのサブクラス
    '''
    class Meta:
        '''UserCreationFormのインナークラス
        
        Attributes:
          model:連携するUserモデル
          fields:フォームで使用するフィールド
        '''
        # 連携するUserモデルを設定
        model = CustomUser
        # フォームで使用するフィールドを設定
        # ユーザー名、メールアドレス、パスワード、パスワード(確認用)
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # usernameの入力をinput type=emailにする
        self.fields["username"].widget = EmailInput()
        self.fields["username"].widget.attrs["class"] = "form-control"

        self.fields["password"].widget.attrs["class"] = "form-control"

class CustomPasswordChangeForm(PasswordChangeForm):
   old_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
   new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
   new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
   def clean_new_password1(self):
       new_password = self.cleaned_data.get('new_password1')
       if len(new_password) < 8:
          raise ValidationError("パスワードは8文字以上である必要があります。")
       return new_password
