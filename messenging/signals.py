from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Message, Thread

from utilities.generators import id_generator


# Create a streaming algorithm for feeding followers and friends on new status arrival


@receiver(pre_save, sender=Message)
def assign_message_id(sender, instance, *args, **kwargs):
    if not instance.id:
        id = id_generator("User")
        instance.id = id


@receiver(pre_save, sender=Thread)
def assign_thread_id(sender, instance, *args, **kwargs):
    if not instance.id:
        id = id_generator("User")
        instance.id = id
