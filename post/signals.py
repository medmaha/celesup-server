from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save
from hashtags.models import HashTag
from .models import Post
from feed.models import Feed

from utilities.generators import id_generator

@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        key = id_generator(used_for='New Post')

        if instance.picture:
            pass

# Create a streaming algorithm for feeding followers and friends on new status arrival
# @receiver(post_save, sender=Post)
def stream_post(sender, instance, created, **kwargs):

    # hashtags = instance.hashtags

    # if hashtags:
    #     for hash in hashtags.split(','):
    #         HashTag.objects.create(
    #             tag=hash.split('#')[0],
    #             object=instance, 
    #             object_id=instance.key
    #         )
            
    
    author = instance.author
    if author.user_type.lower() == 'admin':
        slug = slugify(instance.caption)
        # instance.slug = slug
        instance.key = slugify(id_generator(f'Post'))
        # instance.save()
        return

    feeds = Feed.objects.all()
    profile = author.profile


    friends = profile.friends.all()
    followers = None

    if created and profile.user_type == 'celebrity':
        followers = profile.user_type.followers.all() 

        for friend in friends:
            friend_has_feed = False  
            for feed in feeds:
                if feed.user == friend:
                    
                    #  TODO rewrite the next block --> want to post on the existing feed
                    feed.posts.add(instance)
                    friend_has_feed = True

            if not friend_has_feed:
                id = id_generator(used_for=f'Feed')
                feed = Feed.objects.create(
                    id=id, user=friend,
                    object=instance, 
                    object_id=instance.key
                    )

        for follower in followers:
            if follower in friends:
                continue
            follower_has_feed = False
            for feed in feeds:
                if feed.user == follower:
                    #  TODO rewrite the next block --> want to post on the existing feed
                    feed.posts.add(instance)
                    follower_has_feed = True

            if not follower_has_feed:
                id = id_generator(used_for=f'Feed')
                feed = Feed.objects.create(user=follower, id=id)
                feed.posts.add(instance)

    if created and profile.user_type == 'supporter':
        for friend in friends:
            follower_has_feed = False
            for feed in feeds:
                if feed.user == friend:

                    #  TODO rewrite the next block --> want to post on the existing feed
                    feed.posts.add(instance)
                    follower_has_feed = True
                    
            if not follower_has_feed:
                id = id_generator(used_for='Feed')
                feed = Feed.objects.create(user=friend, id=id)
                feed.posts.add(instance)


        