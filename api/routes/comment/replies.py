from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from post.models import Post
from comment.models import Comment

from api.routes.comment.serializers import CommentSerializer
from api.routes.user.serializers import UserMiniInfoSeriaLizer

from utilities.generators import get_profile_data
from django.shortcuts import get_object_or_404


class PostCommentReplyCreate(CreateAPIView):
    def create(self, request, *args, **kwargs):

        data = request.data.copy()
        post_id = data.get("post")
        parent_comment_id = data.get("parent")

        if not isinstance(request.user, User):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data["author"] = request.user.id
        post = get_object_or_404(Post, key=post_id)
        get_object_or_404(Comment, id=parent_comment_id)

        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(post, serializer)
        self.serializer_class = UserMiniInfoSeriaLizer

        data = {**serializer.data}
        data["author"] = self.get_serializer(post.author).data

        return Response(
            data, status=201, headers=self.get_success_headers(serializer.data)
        )

    def perform_create(self, post, serializer):
        comment = serializer.save()
        comment.activity_rate = +1
        post.activity_rate += 2
        post.author.rating += 1

        comment.save()
        post.save()
        post.author.save()
        return comment


class PostCommentReplyList(ListAPIView):
    def list(self, request, *args, **kwargs):

        comment_id, post_key = str(request.get_full_path()).split("?")[1].split("&")

        post = get_object_or_404(Post, key=post_key.split("=")[1])
        comment = get_object_or_404(Comment, id=comment_id.split("=")[1])

        queryset = Comment.objects.filter(post=post, parent=comment).order_by(
            "created_at"
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            data = self.get_data(serializer)
            return self.get_paginated_response(data)

        serializer = CommentSerializer(queryset, many=True)
        serializer = self.get_data(serializer)
        return Response(data)

    def get_data(self, serializer):
        data = serializer.data
        for comment in data:
            comment["author"] = get_profile_data(User.objects.get(id=comment["author"]))

        return data
