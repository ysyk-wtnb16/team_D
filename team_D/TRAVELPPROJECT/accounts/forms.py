from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CheckboxSelectMultiple, EmailInput
from django.forms import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # 入力項目のリスト
        fields = [
            "email", "name", "zip_code", "address", 
            "myshops", "password1", "password2"]
        # エラーメッセージを指定
        error_messages = {
            "email": {
                # emailが未入力の時のエラーメッセージ
                "required": "このフィールドを入力してください"
            }
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs["placeholder"] = "you@example.com"
        self.fields["email"].widget.attrs["class"] = "form-control ms-5"
        
        self.fields["name"].widget.attrs["class"] = "form-control ms-5"
        
        self.fields["zip_code"].widget.attrs["class"] = "form-control"
        
        self.fields["address"].widget.attrs["class"] = "form-control ms-5"
        
        self.fields["password1"].widget.attrs["class"] = "form-control ms-5"
        
        self.fields["password2"].widget.attrs["class"] = "form-control ms-5"
    
    # emailに対するバリデーション
    def clean_email(self):
        # 入力されたemailを取得
        email = self.cleaned_data["email"]
        # 入力されたemailと一致するemailを持つデータを検索し、件数を求める
        count = CustomUser.objects.filter(email=email).count()
        # 件数が0より大きい=>同じメールアドレスのデータが存在する
        if(count > 0):
            # エラーを発生させる
            raise ValidationError("このメールアドレスは使用できません")
        return email


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # usernameの入力をinput type=emailにする
        self.fields["username"].widget = EmailInput()
        self.fields["username"].widget.attrs["class"] = "form-control"

        self.fields["password"].widget.attrs["class"] = "form-control"


from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm
class PasswordResetForm(AuthPasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs["class"] = "form-control ms-5"