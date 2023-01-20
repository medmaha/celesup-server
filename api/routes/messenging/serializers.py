from rest_framework.serializers import ModelSerializer
from messenging.models import Message, Thread


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "recipient",
            "delivered",
            "is_seen",
            "body",
            "created_at",
        ]


class ThreadSerializer(ModelSerializer):
    class Meta:
        model = Thread
        fields = [
            "id",
            "sender",
            "author",
            "recipient",
            "messages",
            "last_msg",
            "last_msg_date",
        ]
