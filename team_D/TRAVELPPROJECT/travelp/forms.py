from django import forms
from django.forms import ModelForm
from .models import CustomUser, Post, PostImage, Comment, Donation, Fundraising

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'profile_image', 'profile_description']
        widgets = {
            'profile_description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

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

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']
        # amount = forms.IntegerField(label="募金額", min_value=1, max_digits=10)

class FundraisingForm(forms.ModelForm):
    class Meta:
        model = Fundraising
        fields = ['title', 'description', 'goal_amount']
        labels = {
            'title': '　タイトル',
            'description': '説　　明',
            'goal_amount': '目標金額',
        }

    def clean_goal_amount(self):
        goal_amount = self.cleaned_data.get('goal_amount')
        if goal_amount is not None and goal_amount <= 0:
            raise forms.ValidationError("目標金額は1円以上にしてください。")
        return goal_amount

class PaymentForm(forms.Form):
    amount = forms.IntegerField(min_value=1, label="Amount", required=True)
