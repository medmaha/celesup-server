from django.dispatch import receiver
from django.db.models.signals import (post_save, pre_delete, pre_save)

from PIL import Image
from app_features.models import Post, Status
from .generators import id_generator
from celebrity.models import Celebrity
from supporter.models import Supporter

# Resizing Celebrity Profile avater and cover images
@receiver(post_save, sender=Celebrity)
def resize_celebrity_profile_img(sender, instance, created, **kwargs):
    if not created:
        if instance.avater:
            avater = Image.open(instance.avater.path)
            thumbnail = (100, 100)
            avater.thumbnail(thumbnail)
            avater.save(instance.avater.path)
        
        if instance.cover_img:
            cover = Image.open(instance.cover_img)
            if cover.width >= 750:
                cover.thumbnail((750,750))
                cover.save(instance.cover_img.path)
            else:
                cover.thumbnail((550,550))
                cover.save(instance.cover_img.path)
        return 0
    return 1


# Resizing Supporter Profile avater and cover images
@receiver(post_save, sender=Supporter)
def resize_supporter_profile_img(sender, instance, created, **kwargs):
    if not created:
        if instance.avater:
            avater = Image.open(instance.avater.path)
            thumbnail = (100, 100)
            avater.thumbnail(thumbnail)
            avater.save(instance.avater.path)
        
        if instance.cover_img:
            cover = Image.open(instance.cover_img)
            if cover.width >= 750:
                cover.thumbnail((750,750))
                cover.save(instance.cover_img.path)
            else:
                cover.thumbnail((550,550))
                cover.save(instance.cover_img.path)
        print(instance.user)
        return 0
    return 1


# # Resizing Posts that has images
# @receiver(post_save, sender=Post)
# def resize_post_pictures(sender, instance, created, **kwargs):
#     if created and instance.picture:
#         img = Image.open(instance.picture.path)
#         thumbnails = ((750, 750))
#         if img.width >= 800:
#             img.thumbnail(thumbnails)
#             img.save(instance.picture.path)
#         else:
#             img.thumbnail((600, 600))
#             img.save(instance.picture.path)
#         return True


# Status imamge resize
@receiver(post_save, sender=Status)
def resize_status_pictures(sender, instance, created, **kwargs):
    if created and instance.picture:
        img = Image.open(instance.picture.path)
        thumbnails = (600, 600)
        if img.width >= 600:
            img.thumbnail(thumbnails)
            img.save(instance.picture.path)
        else:
            img.thumbnail((500, 500))
            img.save(instance.picture.path)
        
        if instance.caption:
            slug = instance.caption.strip()    
            instance.slug = slug

        instance.key = id_generator(f'Status')
        instance.save()
        return 0
    return 1

