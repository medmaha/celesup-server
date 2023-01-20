from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from post.models import Post
from .serializers import CommentSerializer, CommentCreateSerializer
from django.shortcuts import get_object_or_404
from ..user.serializers import UserMiniInfoSeriaLizer
from comment.models import Comment

class PostCommentCreate(CreateAPIView):
    serializer_class = CommentCreateSerializer
    def create(self, request, *args, **kwargs):

        data = request.data.copy()

        print(data)

        if not isinstance(request.user, User):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        author = request.user
        post = get_object_or_404(Post, key=data.get("post"))
        parent = None
        media_file = None

        if 'parent' in data:
            parent = get_object_or_404(Comment, id=data['parent'])
        
        if 'media' in data:
            media_file = data['media']

        _data = {}

        _data['post'] = post.key 
        _data['author'] = author.id 
        _data['content'] = data['content'] 
        _data['parent'] = parent.id if parent else None
        # _data['media'] = media_file if media_file else None, 


        serializer = self.get_serializer(data=_data)
        serializer.is_valid(raise_exception=True)

        comment = self.perform_create(post, serializer)

        self.serializer_class = CommentSerializer
        comment = self.get_serializer(instance=comment)

        self.serializer_class = UserMiniInfoSeriaLizer
        
        headers = self.get_success_headers(serializer.data)

        return Response(comment.data, status=201, headers=headers)

    def perform_create(self, post, serializer):
        # comment = serializer.save()
        comment = serializer.save()
        post.activity_rate += 1
        post.save()
        post.author.rating += 1
        post.author.save()
        # comment.activity_rate += 1
        # comment.save()

        return comment
