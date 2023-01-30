from comment.models import Comment
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from api.routes.user.serializers import UserMiniInfoSeriaLizer


class CommentParentSerializer(serializers.ModelSerializer):
    author = UserMiniInfoSeriaLizer()
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "author", "parent")

    def get_parent(self, comment):
        if comment.parent:
            comment = comment.parent
            data = {
                "id": comment.id,
                "author": {
                    "id": comment.author.id,
                    "username": comment.author.username,
                },
                "parent": self.get_parent(comment) if comment.parent else None,
            }
            return data
        return None


class CommentSerializer(serializers.ModelSerializer):
    author = UserMiniInfoSeriaLizer()
    replies = RecursiveField(many=True, read_only=True)
    parent = CommentParentSerializer()
    # replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "content",
            "replies",
            "parent",
            "created_at",
            "file",
            "likes",
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("author", "post", "content", "parent", "file")


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "author", "content", "file")
