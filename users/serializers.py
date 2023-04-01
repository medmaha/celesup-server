from rest_framework import serializers
from .models import User


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "avatar", "id"]


class UsersProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "city",
            "avatar",
            "gender",
            "username",
            "cover_img",
            "biography",
            "date_joined",
            "account_type",
            "public_email",
            "email_privacy",
        ]


class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["followers", "friends", "following", "comments"]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "username",
            "avatar",
            "cover",
            "public_email",
            "city",
            "biography",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "avatar", "id"]


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "secondary_email",
            "notification_email",
            "public_email",
            "email_privacy" "date_joined",
            "username",
            "name",
            "avatar",
            "cover",
            "account_rating",
            "gender",
            "city",
            "biography",
            "account_type",
        ]
