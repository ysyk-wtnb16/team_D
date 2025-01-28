#追加した全部
from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

from django.contrib.auth.forms import PasswordChangeForm

from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):

    email = forms.EmailField(required=True)

    nickname = forms.CharField(max_length=50, required=True)

    class Meta:

        model = CustomUser

        fields = ['username', 'nickname', 'email', 'password1', 'password2'] 


class CustomPasswordChangeForm(PasswordChangeForm):
   old_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
   new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
   new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
   def clean_new_password1(self):
       new_password = self.cleaned_data.get('new_password1')
       if len(new_password) < 8:
           raise ValidationError("パスワードは8文字以上である必要があります。")
       return new_password