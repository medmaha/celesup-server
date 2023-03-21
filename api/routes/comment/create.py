from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from post.serializer import PostViewSerializer
from post.models import Post
from django.shortcuts import get_object_or_404
from comment.models import Comment
from comment.serializers import CommentViewSerializer, CommentCreateSerializer


class PostCommentCreate(CreateAPIView):
    serializer_class = CommentCreateSerializer

    def create(self, request, *args, **kwargs):

        data = request.data.copy()

        author = request.user
        post = get_object_or_404(Post, key=data.get("post"))
        parent = None
        media_file = None

        if "parent" in data:
            parent = get_object_or_404(Comment, id=data["parent"])

        if "media" in data:
            media_file = data["media"]

        _data = {}

        _data["post"] = post.key
        _data["author"] = author.id
        _data["content"] = data["content"]
        _data["parent"] = parent.pk if parent else None
        # _data['media'] = media_file if media_file else None,

        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)

        comment = self.perform_create(post, serializer)

        self.serializer_class = CommentViewSerializer
        comment = self.get_serializer(instance=comment)

        headers = self.get_success_headers(serializer.data)

        return Response(comment.data, status=201, headers=headers)

    def perform_create(self, post: Post, serializer: PostViewSerializer):
        comment = serializer.save()
        if post.activity_rate:
            post.activity_rate += 1
        post.save()
        post.author.account_rating += 1
        post.author.save()

        return comment
