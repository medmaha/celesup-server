from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from feed.models import Feed
from rest_framework import status
from post.models import Post
from post.serializer import PostViewSerializer
from users.models import User


class DiscoverPosts(ListAPIView):
    """Gets all post related to the authenticated user"""

    serializer_class = PostViewSerializer

    def get_queryset(self):
        author = self.request.user
        posts = Post.objects.exclude(author=author)
        if not posts.count():
            posts = Post.objects.filter()
        return posts

    def list(self, request, *args, **kwargs):
        if not isinstance(request.user, User):
            return Response(status=status.HTTP_404_NOT_FOUND)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)
