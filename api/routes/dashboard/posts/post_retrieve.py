from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework import status

from post.models import Post
from comment.models import Comment

from .serializers import PostDetailSerializer

from ...user.serializers import UserMiniInfoSeriaLizer, UserDetailSerializer

from utilities.api_utils import get_post_json


class PostRetrieve(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):

        try:
            key = request.get_full_path().split("?")[1].split("=")[1]
            post = get_object_or_404(Post, key=key)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = get_post_json(post, self)

        return Response(
            data,
            status=200,
        )
