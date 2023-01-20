from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView

from post.models import Post
from .serializers import PostDetailSerializer

class PostDelete(DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        key = request.data.get('key')
        instance = get_object_or_404(Post, key=key)
        instance.delete()

        post_title = instance.title.capitalize() if instance.title else 'No Content'

        message = "Successful! post "+ "'" +post_title+ "'" +" has been deleted"

        return Response({'message': message}, status=204)

