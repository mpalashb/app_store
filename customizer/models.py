from PIL import Image
from django.db import models


class HeroCustomizer(models.Model):
    title = models.CharField(max_length=440)
    small_desc = models.TextField()
    right_img = models.ImageField(upload_to="customizer", blank=True)

    def __str__(self):
        return self.title

    def save(self):
        saved = super().save()  # saving image first
        if self.right_img:
            image = Image.open(self.right_img.path)  # Open image using self

            # if img.height > 500 or img.width > 500:
            #     new_img = (500, 500)
            #     img.thumbnail(new_img)
            #     img.save(self.right_img.path)  # saving image at the same path

            resized_im = image.resize(
                (round(image.size[0]*0.25),
                 round(image.size[1]*0.25))
            )
            resized_im.save(self.right_img.path)

        return saved
