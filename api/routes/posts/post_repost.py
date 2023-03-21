from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from post.models import Post
from post.serializer import PostViewSerializer, PostCreateSerializer


class PostRepost(CreateAPIView):
    serializer_class = PostViewSerializer

    def create(self, request, *args, **kwargs):
        user = request.user

        try:
            data = request.data.copy()
            child_post = get_object_or_404(Post, key=data.get("post_id"))
            if data.get("excerpt"):
                post = Post(author=user, excerpt=data.get("excerpt"), child=child_post)
                post.save()
                child_post.shares.add(user)

                serializer = self.get_serializer(post, context={"request": request})

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            pass
        return Response(status=status.HTTP_400_BAD_REQUEST)
