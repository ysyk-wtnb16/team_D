#追加した全部
from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

class SignupForm(UserCreationForm):

    email = forms.EmailField(required=True)

    nickname = forms.CharField(max_length=50, required=True)

    class Meta:

        model = CustomUser

        fields = ['username', 'nickname', 'email', 'password1', 'password2'] 