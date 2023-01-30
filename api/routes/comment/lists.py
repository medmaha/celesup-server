from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from comment.models import Comment
from comment.serializers import CommentViewSerializer

from post.models import Post


class PostCommentList(ListAPIView):
    serializer_class = CommentViewSerializer

    def get_queryset(self, post):
        queryset = Comment.objects.filter(post=post, parent=None)
        return queryset

    def nested_structure(self, comments):
        def get_replies(parent_comment):
            replies = Comment.objects.filter(parent=parent_comment).reverse()[:15]
            for reply in replies:
                reply.replies.set(get_replies(reply))
            return replies

        for comment in comments:
            comment.replies.set(get_replies(comment))

        return comments

    def list(self, request, key, *args, **kwargs):
        post = get_object_or_404(Post, key=key)

        queryset = self.filter_queryset(self.get_queryset(post))

        paginated_comments = self.paginate_queryset(queryset)

        comments = self.nested_structure(paginated_comments)

        serializer = self.get_serializer(
            comments, many=True, context={"request": request}
        )

        return self.get_paginated_response(serializer.data)
