from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from post.models import Post
from post.serializer import PostViewSerializer
from notification.models import Notification


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

            if not post.author == request.user:

                alert = Notification()
                alert.recipient = post.author
                alert.sender = request.user
                alert.action = "Liked your post"
                alert.hint = post.caption or post.excerpt

                save = False
                if alert.hint:
                    alert.hint = alert.hint[:100]
                    save = True
                if post.picture:
                    alert.hint_img = post.picture.file_url
                    save = True

                if save and not Notification.objects.filter(
                    recipient=alert.recipient,
                    sender=alert.sender,
                    action=alert.action,
                    hint=alert.hint,
                    hint_img=alert.hint_img,
                ):
                    alert.save()

        post.save()
        post = Post.objects.get(key=post.key)
        serializer = self.get_serializer(post, context={"request": request})

        return Response(
            serializer.data,
            status=200,
        )
