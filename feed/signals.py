from post.models import Post
from users.models import User
from .models import Feed, FeedObjects
from utilities.generators import id_generator

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_feed_user(sender, created, instance, *args, **kwargs):
    if created:
        feed = Feed(user=instance)
        feed.save()


@receiver(pre_save, sender=Feed)
def assign_feed_id(sender, instance: Feed, *args, **kwargs):

    id_used = False
    id, save_id = id_generator()
    if not instance.id:
        instance.id = id
        id_used = True

    if id_used:
        save_id("Feed for @" + instance.user.email)


# @receiver(post_save, sender=Post)
# def add_to_user_feeds(sender, created, instance, *args, **kwargs):
#     if created:
#         profile = instance.author

#         author_feed, _ = Feed.objects.get_or_create(user=profile)

#         author_feed.posts.add(instance)

#         for user in profile.followers.all():
#             user_feed, created = Feed.objects.get_or_create(user=user)
#             user_feed.posts.add(instance)
