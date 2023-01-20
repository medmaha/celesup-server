from rest_framework import generics
from rest_framework.response import Response

from feed.models import Feed
from rest_framework import status
from post.models import Post, Photo
from ..posts.serializers import PostDetailSerializer, PhotoSerializer
from users.models import User
from utilities.api_utils import get_post_json
from django.shortcuts import get_object_or_404


class FeedPost(generics.ListAPIView):
    """Gets all post related to the authenticated user"""

    def get_queryset(self):

        feed = Feed.objects.get(user=self.request.user)

        if feed.posts.exclude(author=self.request.user).exists():
            queryset = feed.posts.all()
            return queryset

        queryset =  Post.objects.all()[:50]
        
        return queryset

    def list(self, request, *args, **kwargs):
        if not isinstance(request.user, User):
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.serializer_class = PostDetailSerializer

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        feed = []
        for post in serializer.data:
            instance = Post.objects.get(key=post["key"])

            data = instance.get_data(self, PhotoSerializer)
            feed.append({**post, **data})

        return self.get_paginated_response(feed)
