from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status

from .serializers import PostCreateSerializer, PostDetailSerializer, PhotoSerializer
from post.models import Photo, Music, Video, Post


from django.db import transaction


class PostCreate(CreateAPIView):
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if not len(data.keys()):
            return Response(
                "Bad request field required", status=status.HTTP_400_BAD_REQUEST
            )

        data["author"] = request.user.id

        serializer = self.serializer_class(data=self.clean_data(data.copy()))
        serializer.is_valid(raise_exception=True)

        post = self.assign_post_file(data, serializer)

        self.serializer_class = PostDetailSerializer

        post_serializer = self.get_serializer(post)

        data = {**post_serializer.data, **post.get_data(self, PhotoSerializer)}

        return Response({"post": data}, status=status.HTTP_201_CREATED)

    def assign_post_file(self, data, serializer):
        picture = data.get("picture")
        music = data.get("music")
        video, thumbnail = data.get("video"), data.get("thumbnail")

        with transaction.atomic():
            post: Post = serializer.save()

        if picture:
            photo = Photo.objects.create(
                author=post.author, image=picture, alt_text="photo"
            )
            post.picture = photo
            post.save()

        elif music:
            music = Music.objects.create(
                author=post.author,
            )
            post.music = music
            post.save()

        elif video:
            video = Video.objects.create(
                author=post.author, file=video, thumbnail=thumbnail
            )
            post.video = video
            post.save()

            return post

        return post

    def clean_data(self, data):
        if "picture" in data:
            del data["picture"]
        if "video" in data:
            del data["video"]
        if "music" in data:
            del data["music"]
        if "thumbnail" in data:
            del data["thumbnail"]

        return data
