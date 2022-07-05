from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.utils.text import slugify
from .models import AppProduct


@receiver(post_save, sender=AppProduct)
def createSlugPreSig(sender, instance, created, **kwargs):
    if created and not instance.slug:  # thats mean It's created and not being overwrite slug
        instance.slug = slugify(
            f"{instance.name}-{instance.pk}-{uuid.uuid4().hex}")
        instance.save()
