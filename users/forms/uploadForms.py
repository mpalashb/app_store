from django import forms
from apps_app.models import AppProduct, Category, LargeImages
from users.models import MyUser


class UploadAppForm(forms.ModelForm):
    all_large_images = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'multiple': True,
            }), required=False)

    class Meta:
        model = AppProduct
        # exclude = ('author',)
        fields = (
            'name',
            'category',
            'website',
            'desc',
            'thumb_img',
            'all_large_images',)

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control fs-5',
                    'placeholder': 'Title of the app',

                }
            ),
            'category': forms.SelectMultiple(
                attrs={
                    'class': 'form-select form-select-lg',
                    'aria-label': 'form-select-lg example',

                }
            ),
            'website': forms.TextInput(
                attrs={
                    'class': 'form-control fs-5',
                    'placeholder': 'https://example.com',
                }
            ),
            'desc': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'A detailed summary of the description',
                    'rows': '6',
                }
            ),
            'thumb_img': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    # def save(self, commit=True):
    #     apps_saved = super().save(commit)
    #     all_large_images = self.fields.get('all_large_images')
    #     if all_large_images:
    #         for img in all_large_images:
    #             LargeImages_Inc = LargeImages(
    #                 product_id=apps_saved.pk,
    #                 img=img
    #             )
    #             LargeImages_Inc.save()

    #     print('Saved ID', apps_saved.pk)

    #     return apps_saved
