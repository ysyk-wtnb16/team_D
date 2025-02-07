from django.forms import ModelForm
from .models import CustomUser, Post, PostImage, Comment, Donation
from django import forms
 
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'profile_image', 'profile_description']
        widgets = {
            'profile_description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
 
from django import forms
from .models import Post, Fundraising

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'comment', 'caption', 'latitude', 'longitude', 'fundraising']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostCreateForm, self).__init__(*args, **kwargs)

        if user is None or not user.is_staff:
            self.fields.pop('fundraising')
        else:
            self.fields['fundraising'].queryset = Fundraising.objects.all()
            self.fields['fundraising'].required = True

 
class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']
 
 
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
 
# 募金機能
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']
        # amount = forms.IntegerField(label="募金額", min_value=1、max_digits=10)
 
# 市役所
# 募金プロジェクト作成
from .models import Fundraising
class FundraisingForm(forms.ModelForm):
    class Meta:
        model = Fundraising
        fields = ['title', 'description', 'goal_amount']
 
    def clean_goal_amount(self):
        goal_amount = self.cleaned_data.get('goal_amount')
        if goal_amount is not None and goal_amount <= 0:
            raise forms.ValidationError("目標金額は1円以上にしてください。")
        return goal_amount
    

from django import forms
 
class PaymentForm(forms.Form):
    amount = forms.IntegerField(min_value=1, label="Amount", required=True)