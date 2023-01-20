from rest_framework import serializers
from post.models import Post, Photo, Video, Music

from feed.models import FeedObjects


class FeedPost(serializers.ModelSerializer):
    class Meta:
        model = FeedObjects
        fields = ["object"]


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["image", "alt_text"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["file", "title", "description", "thumbnail"]


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
            "thumbnail",
        ]
