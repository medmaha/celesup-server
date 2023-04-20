from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from post.models import Post
from post.serializer import PostViewSerializer, PostCreateSerializer
from notification.models import Notification


class PostRepost(CreateAPIView):
    serializer_class = PostViewSerializer

    def create(self, request, *args, **kwargs):
        user = request.user

        try:
            data = request.data.copy()
            child_post = get_object_or_404(Post, key=data.get("post_id"))

            # post with user thoughts
            if data.get("excerpt"):
                post = Post.objects.create(
                    author=user, excerpt=data.get("excerpt"), child=child_post
                )

            # repost to feeds
            else:
                post = Post.objects.create(author=user, child=child_post)

            child_post.shares.add(user)
            serializer = self.get_serializer(post, context={"request": request})

            user.save()
            alert_1 = Notification()
            alert_1.from_platform = True
            alert_1.recipient = child_post.author
            alert_1.sender = user
            alert_1.action = "Shares your post"
            alert_1.save()
            alert_1.hint = (post.caption or post.excerpt or "",)[0][:100]
            alert_1.hint_img = post.picture.file_url if post.picture else None
            alert_1.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            pass
        return Response(status=status.HTTP_400_BAD_REQUEST)
