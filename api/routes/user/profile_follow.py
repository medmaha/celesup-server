from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from rest_framework import status

from feed.models import Feed, FeedObjects
from users.models import User
from post.models import Post

from .serializers import UserDetailSerializer
from utilities.generators import get_profile_data

from django.db import transaction


class ProfileFollow(GenericAPIView):
    def post(self, request, *args, **kwargs):
        if not isinstance(request.user, User):
            return Response(status=status.HTTP_404)
        profile = get_object_or_404(User, id=request.data.get("profile_id"))
        user = request.user

        if user.id == profile.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user in profile.followers.all():
            profile.followers.remove(user)
            user.following.remove(profile)

            FollowThread(profile, user, "onFollow")

        else:
            profile.followers.add(user)
            user.following.add(profile)

            FollowThread(profile, user)

        self.serializer_class = UserDetailSerializer

        profile_data = get_profile_data(profile)
        serializer = self.get_serializer(profile).data

        data = {**profile_data, **serializer}

        return Response(data, status=status.HTTP_200_OK)


import threading


class FollowThread(threading.Thread):
    def __init__(self, profile: User, user: User, task="Follow"):
        self.profile = profile
        self.user = user
        self.task_action = task
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        client_feed = Feed.objects.get(user=self.user)

        with transaction.atomic():
            user_posts = Post.objects.filter(author=self.profile)
            if self.task_action == "Follow":
                for post in user_posts:
                    client_feed.posts.add(post)

                self.profile.rating += 2
                self.profile.save()

            elif self.task_action == "onFollow":
                user_posts = client_feed.posts.filter(author=self.profile)
                for post in user_posts:
                    client_feed.posts.remove(post)
                    post.feed_set.clear()

                self.profile.rating -= 1
                self.profile.save()
