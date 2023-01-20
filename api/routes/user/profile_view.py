from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from users.models import User
from post.models import Post
from utilities.generators import get_profile_data
from api.routes.user.serializers import UserDetailSerializer


class ProfileView(GenericAPIView):

    serializer_class = UserDetailSerializer

    # ? Another user profile
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")

        user = get_object_or_404(User, username__iexact=username)

        profile = get_profile_data(user)
        serializer = self.get_serializer(user).data

        data = {**profile, **serializer, "posts": self.posts_count(user)}
        return Response(data, status=200)

    # ? own profile
    def get(self, request, *args, **kwargs):
        user = request.user

        if not isinstance(user, User):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        profile = get_profile_data(user)
        serializer = self.get_serializer(user).data

        data = {**profile, **serializer, "posts": self.posts_count(user)}
        return Response(data, status=200)

    def posts_count(self, author):
        return Post.objects.filter(author=author).count()
