from dataclasses import field
# from ckeditor.widgets import CKEditorWidget

from django.contrib import admin
from django import forms
from .models import (Category,
                     AppProduct,
                     LargeImages,)


class AppAdminForm(forms.ModelForm):
    # desc = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = AppProduct
        fields = "__all__"
        # widgets = {
        #     'desc': forms.Textarea(attrs={'class': 'ckeditor'}),
        # }


class AppProductImagesInline(admin.TabularInline):
    model = LargeImages


class AppProductAdmin(admin.ModelAdmin):
    form = AppAdminForm
    inlines = [
        AppProductImagesInline,
    ]


admin.site.register(Category)
admin.site.register(LargeImages)
admin.site.register(
    AppProduct,
    AppProductAdmin
)
