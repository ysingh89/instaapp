from django import forms
from .models import Posts, Users

class Login(forms.Form):
    username = forms.CharField(label='Use name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class UserSignUp(forms.ModelForm):
    class Meta:
        model = Users
        fields = [
            "username",
            "password",
            "userimage",
            "fname",
            "lname",
            "phone",
            "email"
        ]

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            "title",
            'image'
        ]
