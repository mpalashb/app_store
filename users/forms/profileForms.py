from django import forms
from ..profileModels import ProfileModel


class ProfileForms(forms.ModelForm):
    class Meta:
        model = ProfileModel
        exclude = ("user_ac", )
        # fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
