from rest_framework.generics import GenericAPIView
from rest_framework import status

from comment.models import Comment

from api.routes.dashboard.posts.serializers import PostDetailSerializer
from api.routes.user.serializers import UserMiniInfoSeriaLizer

from utilities.generators import get_profile_data


def get_post_json(post, view: GenericAPIView) -> dict:

    view.serializer_class = PostDetailSerializer
    post_comments = Comment.objects.filter(post=post)

    post_serializer = view.get_serializer(post).data

    view.serializer_class = UserMiniInfoSeriaLizer

    post_comments = Comment.objects.filter(post=post)

    data = {
        **post_serializer,
        "key": post.key,
        "bookmarks": 0,
        "comments": post_comments.count(),
        "shares": post.shares.all().count(),
        "likes": view.get_serializer(post.likes.all(), many=True).data,
    }

    data["author"] = {
        **get_profile_data(post.author),
        **view.get_serializer(post.author).data,
    }

    return data
