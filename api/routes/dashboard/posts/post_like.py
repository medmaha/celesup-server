from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from post.models import Post
from .serializers import PostDetailSerializer, PhotoSerializer

from utilities.api_utils import get_post_json
from comment.models import Comment
from feed.models import FeedObjects
from api.routes.user.serializers import UserDetailSerializer


class LikePost(GenericAPIView):

    serializer_class = PostDetailSerializer

    def post(self, request, *args, **kwargs):

        post_key = request.data.get("post_key")
        post = get_object_or_404(Post, key=post_key)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.activity_rate -= 1
            post.save()
        else:
            post.likes.add(request.user)
            post.activity_rate += 2
            post.save()

        data = post.get_data(self, PhotoSerializer)

        return Response(
            data,
            status=200,
        )
