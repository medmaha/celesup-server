from rest_framework.serializers import ModelSerializer
from notification.models import Notification


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "sender",
            "recipient",
            "action",
            "hint",
            "hint_img",
            "is_viewed",
            "created_at",
        ]


class NotificationUpdateSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "is_viewed",
        ]
