from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from hashtags.models import HashTag
from post.models import Post
from django.utils.text import slugify

from utilities.generators import id_generator


# Create a streaming algorithm for feeding followers and friends on new status arrival


@receiver(pre_save, sender=HashTag)
def assign_user_id(sender, instance, *args, **kwargs):
    id, callback = id_generator()

    instance.id = id
    callback("Hashtag")


@receiver(post_save, sender=Post)
def stream_post(sender, instance, created, **kwargs):
    hashtag = instance.hashtags

    if not hashtag:
        return

    hashtags = hashtag.split(",")

    for tag in hashtags:
        try:
            __tag = tag.split("#")[1].strip().lower()
        except:
            __tag = tag.strip().lower()

        __tag = slugify(tag)
        # existing_hashtags = HashTag.objects.filter(tag_text=__tag).exists()

        # # # TODO add hashtag object to the matching tag
        # if existing_hashtags:
        #     continue

        HashTag.objects.create(tag_text=__tag, object=instance, object_id=instance.key)
