from django.db import models
from PIL import Image
from .models import MyUser


class ProfileModel(models.Model):
    user_ac = models.OneToOneField(
        to=MyUser, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=220)
    avatar = models.ImageField(upload_to="avatar", blank=True)

    def save(self):
        saved = super().save()  # saving image first
        if self.avatar:
            img = Image.open(self.avatar.path)  # Open image using self

            if img.height > 400 or img.width > 400:
                new_img = (400, 400)
                img.thumbnail(new_img)
                img.save(self.avatar.path)  # saving image at the same path

        return saved

    def __str__(self) -> str:
        return self.name
