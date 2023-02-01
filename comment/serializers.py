from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Comment
from users.serializers import UserViewSerializer


class CommentParentSerializer(serializers.ModelSerializer):
    author = UserViewSerializer()
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "author", "parent")

    def get_parent(self, comment):
        if comment.parent:
            comment = comment.parent
            data = {
                "id": comment.id,
                "author": UserViewSerializer(comment.author).data,
                "parent": self.get_parent(comment) if comment.parent else None,
            }
            return data
        return None


class CommentViewSerializer(serializers.ModelSerializer):
    author = UserViewSerializer()
    replies = RecursiveField(many=True, read_only=True)
    parent = CommentParentSerializer()

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
        fields = ("id", "content", "file")
