from rest_framework import serializers

from users.models import User

from .models import Post
from photo.serializers import PhotoViewSerializer
from users.serializers import UserViewSerializer
from comment.serializers import CommentViewSerializer
from comment.models import Comment

 
class PostViewSerializer(serializers.ModelSerializer):
    author = UserViewSerializer()
    picture = PhotoViewSerializer()
    stats = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    child = serializers.SerializerMethodField()

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
            "child",
            "client",
        ]

    def get_client(self, obj: Post):

        data = {"saved": False}
        request = self.context.get("request")

        if request and request.user:
            user: User = request.user
            data["liked"] = user in obj.likes.all()
            data["shared"] = user in obj.shares.all()
            data["commented"] = Comment.objects.filter(
                author=user, post=obj, parent=None
            ).exists()

        return data

    def get_stats(self, obj: Post):

        # todo create object.is_child attribute instead on this expensive queries
        child = Post.objects.filter(child=obj)

        # if child:
        #     return {}

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

    def get_child(self, obj: Post):
        if obj.child:
            child = PostViewSerializer(obj.child, context=self.context)

            data = child.data.copy()

            del data["stats"]
            del data["child"]
            del data["client"]
            del data["created_at"]
            return data

    @property
    def data(self):
        _data = dict(super().data)
        post: Post = Post.objects.get(key=_data.get("key"))

        if post.child:
            _data = {
                "key": _data.get("key"),
                "author": _data.get("author"),
                "hashtags": _data.get("hashtags"),
                "excerpt": _data.get("excerpt"),
                "stats": _data.get("stats"),
                "created_at": _data.get("created_at"),
                "client": _data.get("client"),
                "child": {
                    "key": _data.get("key"),
                    "author": _data.get("author"),
                    "hashtags": _data.get("hashtags"),
                    "picture": _data.get("picture"),
                    "excerpt": _data.get("excerpt"),
                },
            }
            return _data
        return _data



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




class PostStatSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    shares = serializers.SerializerMethodField()
    comments = CommentViewSerializer()
    bookmarks = serializers.SerializerMethodField()
    child = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "likes",
            "shares",
            "comments",
            "bookmarks",
        ]

    def get_likes(self, obj: Post):
        return UserViewSerializer(obj.likes.all(), many=True, context=self.context).data

    def get_shares(self, obj: Post):
        return UserViewSerializer(
            obj.shares.all(), many=True, context=self.context
        ).data

    def get_bookmark(self, obj: Post):
        return []

    def data(self):
        _data = super().data

        # todo create object.is_child attribute instead on these expensive queries

        post = Post.objects.get(key=_data.get("key"))
        child = Post.objects.filter(child=post)

        if child.first():
            return {}

        return _data

