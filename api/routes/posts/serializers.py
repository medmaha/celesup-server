from rest_framework import serializers

# from post.models import Post, Photo, Video, Music
from post.models import Post
from photo.models import Photo
from ..user.serializers import UserMiniInfoSeriaLizer

from feed.models import FeedObjects


class FeedPost(serializers.ModelSerializer):
    class Meta:
        model = FeedObjects
        fields = ["object"]


class PhotoSerializer(serializers.ModelSerializer):
    width = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["url", "alt_text", "width", "height"]

    def get_url(self, photo: Photo):
        return photo.image.url

    def get_width(self, photo: Photo):
        return photo.width

    def get_height(self, photo: Photo):
        return photo.width

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)


# class VideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Video
#         fields = ["file", "title", "description", "thumbnail"]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "author",
            "excerpt",
            "hashtags",
            "caption",
            "picture",
            "video",
            "thumbnail",
        ]


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["key", "excerpt", "caption"]


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserMiniInfoSeriaLizer()
    # picture = PhotoSerializer()

    class Meta:
        model = Post
        fields = fields = [
            "key",
            "author",
            "caption",
            "excerpt",
            "hashtags",
            "video",
            "picture",
            "created_at",
        ]
