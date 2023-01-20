from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from users.models import User
from admin_users.models import Admin

from celebrity.models import Celebrity
from supporter.models import Supporter

from utilities.generators import id_generator
from django.db import transaction


@receiver(pre_save, sender=User)
def assign_user_id(sender, instance: User, *args, **kwargs):
    try:
        User.objects.get(email=instance.email)
    except:
        id = id_generator("User")
        instance.notification_email = instance.email
        instance.id = id

    if instance.first_name:
        instance.first_name = instance.first_name.capitalize()
    if instance.last_name:
        instance.last_name = instance.last_name.capitalize()
    if instance.city:
        instance.city = instance.city.capitalize()
    if instance.username:
        instance.username = instance.username.capitalize()
    if instance.biography:
        instance.biography = instance.biography.capitalize()
    if instance.gender:
        instance.gender = instance.gender.capitalize()


@receiver(post_save, sender=User)
def differentiate_user_types(sender, instance, created, **kwargs):
    if created:
        if instance.user_type.lower().startswith("cel"):
            Celebrity.objects.create(user=instance, id=instance.id)

        elif instance.user_type.lower().startswith("sup"):
            Supporter.objects.create(user=instance, id=instance.id)

        elif instance.user_type.lower() == ("admin"):
            Admin.objects.create(user=instance)

        else:
            Supporter.objects.create(user=instance, id=instance.id)
