import json
from django.urls import re_path
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from users.models import User
from messenging.models import Thread

from .serializers import MessageSerializer
from ..user.serializers import UserMiniInfoSeriaLizer


USER_GROUPS = []


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.thread_id = self.scope["query_string"].decode("utf-8").split("=")[1]
        self.group_name = self.thread_id + "__thread"

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def send_handshake(self, event):
        self.send(text_data=json.dumps(event))

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        event = {"type": "chat_message", "message": data["message"]}
        async_to_sync(self.channel_layer.group_send)(self.group_name, event)

    def chat_message(self, event):
        thread = Thread.objects.get(id=self.thread_id)
        queryset = thread.messages.all().order_by("created_at")
        serializer = MessageSerializer(instance=queryset, many=True)

        for data in serializer.data:
            sender = UserMiniInfoSeriaLizer(User.objects.get(id=data["sender"])).data
            recipient = UserMiniInfoSeriaLizer(
                User.objects.get(id=data["recipient"])
            ).data
            data["sender"] = sender
            data["recipient"] = recipient

        self.send(json.dumps({"data": serializer.data, "type": "ChatList"}))


message_ws_urlpatterns = [
    re_path(r"ws/chat/threads", ChatConsumer.as_asgi()),
]
