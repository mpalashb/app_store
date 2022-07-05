from django import forms
from django.contrib.auth.password_validation import password_validators_help_text_html, password_validators_help_texts

from django.contrib.auth.forms import UserCreationForm
from users.models import MyUser


class UserCreationFormExtend(UserCreationForm):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control py-2',
            'required': True,
            'placeholder': 'Password'
        }
    ),
        strip=False,
        help_text=password_validators_help_text_html(),
    )
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control py-2',
            'required': True,
            'placeholder': 'Confirm'

        }
    ),
        strip=False,
        help_text="Enter the same password as before, for verification"

    )

    class Meta:
        model = MyUser
        fields = (
            "email",
            "password1",
            "password2",
        )
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control py-2',
                'required': True,
                'placeholder': 'Email'
            }),
        }
