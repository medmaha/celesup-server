from django.db import transaction
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from photo.serializers import PhotoCreateSerializer

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
        serializer = self.get_serializer(data=clean_data)
        serializer.is_valid(raise_exception=True)

        post = self.create_media(data, serializer)

        self.serializer_class = PostViewSerializer

        post_serializer = self.get_serializer(post, context={"request": request})

        data = post_serializer.data

        return Response({"post": data}, status=status.HTTP_201_CREATED)

    def create_media(self, data, serializer):
        with transaction.atomic():
            post: Post = serializer.save()

        media = data.get("media")
        if not media:
            return post

        try:
            print(data)
            picture = media.get("picture")

            if picture and len(picture) > 3:
                img_serializer = PhotoCreateSerializer(data=picture)
                img_serializer.is_valid(raise_exception=True)

                picture_data: dict = picture
                photo = Photo(
                    author_id=post.author.id,
                    file_url=picture_data.get("url"),
                    name=picture_data.get("picture_name"),
                    width=picture_data.get("width"),
                    height=picture_data.get("height"),
                    alt_text=picture_data.get("alt_text") or "post alt text",
                    used_for="post",
                )
                photo.save()
                post.picture = photo
                post.save()

            return post
        except Exception as e:
            post.delete()
            print(e)
            raise e

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
