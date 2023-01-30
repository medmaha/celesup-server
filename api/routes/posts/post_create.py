from django.db import transaction
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status

from post.models import Photo, Post
from post.serializer import PostViewSerializer, PostCreateSerializer


class PostCreate(CreateAPIView):
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if not len(data.keys()):
            return Response(
                "Bad request field required", status=status.HTTP_400_BAD_REQUEST
            )

        data["author"] = request.user.id

        clean_data = self.clean_media_files(data)
        serializer = self.serializer_class(data=clean_data)
        serializer.is_valid(raise_exception=True)

        post = self.create_media(data, serializer)

        self.serializer_class = PostViewSerializer

        post_serializer = self.get_serializer(post, context={"request": request})

        return Response({"post": post_serializer.data}, status=status.HTTP_201_CREATED)

    def create_media(self, data, serializer):
        picture = data.get("picture")
        # music = data.get("music")
        # video, thumbnail = data.get("video"), data.get("thumbnail")

        with transaction.atomic():
            post: Post = serializer.save()

        if picture:
            photo = Photo.objects.create(
                author=post.author,
                file=picture,
                alt_text="photo " + post.author.username,
            )
            post.picture = photo
            post.save()

        return post

    def clean_media_files(self, data):
        data = data.copy()
        if "picture" in data:
            del data["picture"]
        if "video" in data:
            del data["video"]
        if "music" in data:
            del data["music"]
        if "thumbnail" in data:
            del data["thumbnail"]

        return data
