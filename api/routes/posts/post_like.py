from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from post.models import Post
from post.serializer import PostViewSerializer
 

class LikePost(GenericAPIView):

    serializer_class = PostViewSerializer

    def post(self, request, *args, **kwargs):

        post_key = request.data.get("post_key")
        post = get_object_or_404(Post, key=post_key)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            if post.activity_rate:
                post.activity_rate -= 1
            post.author.account_rating -= 1
        else:
            post.likes.add(request.user)
            if post.activity_rate:
                post.activity_rate += 1
            post.author.account_rating += 1

        post.save()
        post = Post.objects.get(key=post.key)
        serializer = self.get_serializer(post, context={'request':request})


        return Response(
            serializer.data,
            status=200,
        )
