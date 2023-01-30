from rest_framework import serializers

from .models import Post
from photo.serializers import PostViewSerializer
from users.serializers import UserViewSerializer
from comment.serializers import CommentViewSerializer
from comment.models import Comment


class PostViewSerializer(serializers.ModelSerializer):
    author = UserViewSerializer()
    picture = PostViewSerializer()
    stats = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            # "id",
            "key",
            "author",
            "caption",
            "excerpt",
            "hashtags",
            "picture",
            "created_at",
            "stats",
            "client",
        ]

    def get_client(self, obj: Post):
        data = {
            "saved": False,
            "liked": self.context.get("request").user in obj.likes.all(),
            "shared": self.context.get("request").user in obj.shares.all(),
            "commented": Comment.objects.filter(
                author=self.context.get("request").user, post=obj, parent=None
            ).exists(),
        }
        return data

    def get_stats(self, obj: Post):
        data = {
            "likes_count": obj.likes.count(),
            "shares_count": self.get_share_count(obj),
            "comments_count": self.get_comments_count(obj),
            "bookmarks_count": self.get_bookmark_count(obj),
        }
        return data

    def get_share_count(self, obj):
        return obj.shares.count()

    def get_comments_count(self, obj: Post):
        return Comment.objects.filter(post=obj).count()

    def get_bookmark_count(self, obj: Post):
        return 3


class PostStatsSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    shares = serializers.SerializerMethodField()
    comments = CommentViewSerializer(many=True)
    bookmarks = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "likes",
            "shares",
            "comments",
            "bookmarks",
        ]

    def get_likes(self, obj: Post):
        return UserViewSerializer(obj.likes.all(), many=True).data

    def get_shares(self, obj: Post):
        return []

    def get_bookmark(self, obj: Post):
        return []


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "author",
            "caption",
            "excerpt",
            "hashtags",
        ]


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "key",
            "caption",
            "excerpt",
            "hashtags",
            "picture",
        ]
