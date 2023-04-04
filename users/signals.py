from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete
from photo.models import Photo

from PIL import Image
import re
import os

from users.models import User

from administrator.models import Administrator

from celebrity.models import Celebrity
from supporter.models import Supporter

from utilities.generators import id_generator

from photo.models import Photo


@receiver(pre_save, sender=User)
def assign_user_id(sender, instance: User, **kwargs):
    id, save_id = id_generator()
    id_used = False
    if not instance.pk:
        instance.username = instance.username.lower()
        instance.notification_email = instance.email
        instance.id = id
        id_used = True

    if id_used:
        save_id("User @" + instance.username)

        # Todo resize images

    if instance.name:
        instance.name = instance.name.capitalize()

    if instance.city:
        instance.city = instance.city.capitalize()

    if instance.biography:
        instance.biography = instance.biography.capitalize()


@receiver(post_save, sender=User)
def set_account_profile(sender, instance, created, **kwargs):
    if created:
        match instance.account_type.lower():
            case "celebrity":
                Celebrity.objects.create(user=instance, id=instance.id)
            case "supporter":
                Supporter.objects.create(user=instance, id=instance.id)
            case "administrator":
                Administrator.objects.create(user=instance, id=instance.id)


# @receiver(pre_delete, sender=User)
def delete_photo(sender, instance: Photo, **kwargs):
    """
    deletes all the user's photo right before the the user is delete
    """

    photos_by_user = Photo.objects.filter(author=instance)

    for photo in photos_by_user:

        file_path = photo.file.path
        found_default_path = re.search(
            r"default.(a|c|n|p|v)*\w{0,}(-|_)?\w{0,}?\.", file_path
        )

        if found_default_path is not None:
            continue

        try:
            image = Image.open(file_path)
            os.remove(image.filename)
            # photo.delete()
        except Exception as e:
            print(e)
