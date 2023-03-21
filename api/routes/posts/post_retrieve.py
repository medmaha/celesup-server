from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from post.models import Post
from post.serializer import PostViewSerializer


class PostRetrieve(RetrieveAPIView):
    serializer_class = PostViewSerializer

    def retrieve(self, request, *args, **kwargs):

        try:
            key = request.get_full_path().split("?")[1].split("=")[1]
            post = get_object_or_404(Post, key=key)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        post_serializer = self.get_serializer(post, context={"request": request})

        data = post_serializer.data

        return Response(data, status=status.HTTP_200_OK)
