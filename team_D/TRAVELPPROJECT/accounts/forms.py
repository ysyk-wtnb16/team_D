# UserCreationFormクラスをインポート
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import CheckboxSelectMultiple, EmailInput
# models.pyで定義したカスタムUserモデルをインポート
from .models import CustomUser

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