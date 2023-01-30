from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework.response import Response


from comment.models import Comment
from post.models import Post


class PostStatistics(ListAPIView):
    """Gets all post related to the authenticated user"""

    def list(self, request, *args, **kwargs):

        post_key = request.get_full_path().split("?")[1].split("=")[1]
        post = get_object_or_404(Post, key=post_key)

        post_comments = Comment.objects.filter(post=post)

        data = {}

        data["likes"] = post.likes.all().count()
        data["comments"] = post_comments.count()
        data["shares"] = 0

        return Response(data, status=200)
