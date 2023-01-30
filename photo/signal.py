from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Photo

from PIL import Image
import os


@receiver(pre_delete, sender=Photo)
def delete_photo(sender, instance: Photo, **kwargs):
    """
    deletes all the user's photo right before the the user is delete
    """

    photos_by_user = Photo.objects.filter(author=instance.author)

    for photo in photos_by_user:
        file_path = photo.file.path
        try:
            image = Image.open(file_path)
            os.remove(image.filename)
        except Exception as e:
            print(e)
