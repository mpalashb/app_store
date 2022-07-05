from django.db import models
from users.models import MyUser
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return str(self.name)


class AppProduct(models.Model):
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='all_apps')
    name = models.CharField(max_length=220)
    slug = models.SlugField(max_length=440, blank=True)
    category = models.ManyToManyField(
        Category, related_name='all_apps')
    website = models.CharField(max_length=250, blank=True)
    desc = models.TextField(blank=True)
    thumb_img = models.ImageField(
        upload_to="thumb", blank=True)

    def __str__(self) -> str:
        return str(self.name)

    def save(self):
        saved = super().save()  # saving image first

        if self.thumb_img:
            img = Image.open(self.thumb_img.path)  # Open image using self

            if img.height > 300 or img.width > 300:
                new_img = (300, 300)
                img.thumbnail(new_img)
                img.save(self.thumb_img.path)  # saving image at the same path
        return saved


class LargeImages(models.Model):
    product_id = models.ForeignKey(
        AppProduct, on_delete=models.CASCADE, related_name='all_large_images'
    )
    img = models.ImageField(upload_to="images")

    def __str__(self) -> str:
        return str(self.product_id.name)

    def save(self):
        saved = super().save()  # saving image first

        if self.img:
            image = Image.open(self.img.path)  # Open image using self

            resized_im = image.resize(
                (round(image.size[0]*0.25),
                 round(image.size[1]*0.25))
            )
            resized_im.save(self.img.path)
        return saved
