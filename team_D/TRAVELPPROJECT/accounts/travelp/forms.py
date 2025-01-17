from django import forms

class PostForm(forms.Form):
    title = forms.CharField(max_length=50)
    name = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)

