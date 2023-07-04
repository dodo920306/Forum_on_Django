from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, Post


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=False, label='電子信箱')
    nickname = forms.CharField(required=False, label='暱稱')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nickname']
        labels = {
            'username': '帳號',
            'password1': '密碼',
            'password2': '確認密碼',
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['board', 'title', 'content', 'image']
        labels = {
            'board': '選擇看板',
            'title': '標題',
            'content': '內容',
            'image': '附圖 (可選)'
        }
        widgets = {
            'image': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
