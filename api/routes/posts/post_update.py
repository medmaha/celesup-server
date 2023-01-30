
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from post.models import Post
from .serializers import (
    PostUpdateSerializer, PostDetailSerializer
)        

class PostUpdate(UpdateAPIView):


    serializer_class = PostUpdateSerializer
    def update(self, request, *args, **kwargs):
        key = request.data.get('key')
        print(request.data)
        instance = get_object_or_404(Post, key=key)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(PostDetailSerializer(instance).data, status=200)


    def patch(self, request, *args, **kwargs):
        return Response({"detail": 'method "PATCH" not allowed'}, status=405)
