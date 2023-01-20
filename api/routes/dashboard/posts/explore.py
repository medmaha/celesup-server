from rest_framework import generics
from rest_framework.response import Response

from feed.models import Feed
from rest_framework import status
from post.models import Post
from .serializers import PostDetailSerializer, PhotoSerializer
from users.models import User
from utilities.api_utils import get_post_json
from django.shortcuts import get_object_or_404


class ExplorePosts(generics.ListAPIView):
    """Gets all post related to the authenticated user"""

    def get_queryset(self):
        author = self.request.user
        posts = Post.objects.exclude(author=author)
        if not posts.count():
            posts = Post.objects.filter()
        return posts

    def list(self, request, *args, **kwargs):
        if not isinstance(request.user, User):
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.serializer_class = PostDetailSerializer

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        discovers = []
        for post in serializer.data:
            instance = Post.objects.get(key=post["key"])

            data = instance.get_data(self, PhotoSerializer)
            discovers.append({**post, **data})

        return self.get_paginated_response(discovers)
