from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=220, widget=forms.EmailInput(
        attrs={'class': 'form-control py-2', 'required': True, 'placeholder': 'Email'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control py-2', 'required': True, 'placeholder': 'Password'}))
