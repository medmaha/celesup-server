from rest_framework import serializers
from users.models import User
from admin_users.models import Admin

from supporter.models import Supporter
from celebrity.models import Celebrity


class UserMETADATASeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserMiniInfoSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "avatar", "full_name", "username", "public_email", "user_type"]


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "avatar",
            "city",
            "gender",
            "email_2",
            "email_3",
            "cover_img",
            "biography",
            "last_name",
            "first_name",
            "public_email",
            "email_privacy",
            "notification_email",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            # ? identifiers
            "id",
            "city",
            "avatar",
            "gender",
            "username",
            "full_name",
            "cover_img",
            "biography",
            # ? activities
            "posts_count",
            # "share_count",
            # "posts_count",
            # "bookmark_count",
            # "friends_count",
            # "followers_count",
            # "following_count",
            "followers",
            "following",
            "user_type",
            # ? emails
            "email",
            "email_2",
            "email_3",
            "public_email",
            "email_privacy",
            "notification_email",
            # ? dates
            "date_joined",
        ]


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "avatar",
            "email",
            "username",
            "first_name",
            "last_name",
            "gender",
            "city",
            "biography",
            "user_type",
        ]


class CelebritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Celebrity
        fields = ["friends", " profile_type"]


class SupporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supporter
        fields = ["profile_type"]


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["profile_type"]
