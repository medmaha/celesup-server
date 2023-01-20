from django.shortcuts import get_object_or_404
from rest_framework import generics

from users.models import User
from post.models import Post
from .serializers import PostDetailSerializer
from utilities.generators import get_profile_data
from utilities.api_utils import get_post_json
from comment.models import Comment
from api.routes.user.serializers import UserDetailSerializer


class PostsList(generics.ListAPIView):
    """Gets all post related to the authenticated user"""

    serializer_class = PostDetailSerializer

    def list(self, request, *args, **kwargs):

        try:
            path = request.get_full_path()
            user_id = path.split("?")[1].split("=")[1]

            print(user_id)
            user = get_object_or_404(User, id=user_id)
            self.queryset = (
                Post.objects.filter(author=user).order_by("-created_at").distinct()
            )
        except:
            self.queryset = Post.objects.filter().order_by("-created_at").distinct()

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        posts = []
        for post in serializer.data:
            instance = Post.objects.get(key=post["key"])

            data = get_post_json(instance, self)
            posts.append({**post, **data})

        return self.get_paginated_response(posts)
