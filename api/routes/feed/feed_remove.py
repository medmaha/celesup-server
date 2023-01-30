from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from feed.models import Feed
from rest_framework import status
from users.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction
import threading


class FeedRemove(GenericAPIView):
    def post(self, request, *args, **kwargs):

        data = request.data.copy()
        if not isinstance(request.user, User):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        profile = get_object_or_404(User, id=data.get("post_author_id"))

        if profile.id == user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        FeedThread(user, profile)
        # client_feed = Feed.objects.get(user=client)
        # posts = client_feed.posts.filter(author=profile)
        # client_feed.posts.remove(posts)

        return Response(status=status.HTTP_200_OK)


class FeedThread(threading.Thread):
    def __init__(self, user: User, profile: User):
        self.user = user
        self.profile = profile
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        with transaction.atomic():

            if self.user in self.profile.followers.all():
                self.profile.followers.remove(self.user)
                self.user.following.remove(self.profile)

            user_feed = Feed.objects.get(user=self.user)
            posts = user_feed.posts.filter(author=self.user)

            for p in posts:
                user_feed.posts.remove(p)
                p.feed_set.clear()

            self.profile.rating -= 1
            self.profile.save()
