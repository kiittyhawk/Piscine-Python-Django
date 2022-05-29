
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={
        'class':'form-input'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class':'form-input'
    }))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={
        'class':'form-input'
    }))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        
