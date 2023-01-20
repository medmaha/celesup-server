from post.models import Post
from users.models import User
from .models import Feed, FeedObjects
from utilities.generators import id_generator

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


@receiver(pre_save, sender=Feed)
def assign_feed_id(sender, instance, *args, **kwargs):
    if not instance.id:
        feed_id = id_generator("Feed User")
        instance.id = feed_id


# @receiver(pre_save, sender=FeedObjects)
# def assign_feed_id(sender, instance, *args, **kwargs):
#     if not instance.id:
#         feed_id = id_generator("Feed Item")
#         instance.id = feed_id


@receiver(post_save, sender=User)
def new_feed(sender, created, instance, *args, **kwargs):
    if created:
        feed_id = id_generator("Feed User")
        Feed.objects.create(id=feed_id, user=instance)


@receiver(post_save, sender=Post)
def add_to_user_feeds(sender, created, instance, *args, **kwargs):
    if created:
        profile = instance.author

        author_feed, _ = Feed.objects.get_or_create(user=profile)

        author_feed.posts.add(instance)

        for user in profile.followers.all():
            user_feed, created = Feed.objects.get_or_create(user=user)
            user_feed.posts.add(instance)
