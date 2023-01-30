from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from feed.models import Feed
from rest_framework import status
from users.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction
from post.models import Post
import threading


class FeedNotInterested(GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if not isinstance(request.user, User):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        post = get_object_or_404(Post, key=data.get("post_key"))

        FeedThread(user, post)
        return Response(status=status.HTTP_200_OK)


class FeedThread(threading.Thread):
    def __init__(self, user: User, post: Post):
        self.user = user
        self.post = post
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        with transaction.atomic():
            user_feed, _ = Feed.objects.get_or_create(user=self.user)
            user_feed.posts.remove(self.post)
