from rest_framework import generics

from feed.models import Feed
from post.models import Post

from post.serializer import PostViewSerializer
from django.contrib.sites.shortcuts import get_current_site


class FeedPost(generics.ListAPIView):
    """Gets all post related to the authenticated user"""

    serializer_class = PostViewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):

        feed = Feed.objects.get(user=self.request.user)

        if feed.posts.exclude(author=self.request.user).exists():
            queryset = feed.posts.all()
            return queryset

        queryset = Post.objects.all()[:50]

        return queryset

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True, context={"request": request})

        return self.get_paginated_response(serializer.data)
