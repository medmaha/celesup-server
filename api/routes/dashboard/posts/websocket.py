import json
from asgiref.sync import async_to_sync
from django.urls import re_path
from channels.generic.websocket import WebsocketConsumer
from .serializers import PostDetailSerializer
from post.models import Post


class PostActivitiesConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "posts"

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

        self.send(json.dumps({"conn": "established"}))


class PostMonitorConsumer(WebsocketConsumer):
    def connect(self):
        self.post_id = str(self.scope["query_string"].decode("utf-8").split("=")[1])
        self.group_name = "post___" + self.post_id
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        event = {"type": "handle_post"}

        print(self.scope)
        print(self.channel_receive)

        if data.get("type") == "POST_LIKE":
            async_to_sync(self.channel_layer.group_send)(self.group_name, event)

    def handle_post(self, event):
        self.send(json.dumps({"type": "POST_ACTIVITY"}))


post_ws_urlpatterns = [
    re_path(r"ws/post/activities", PostActivitiesConsumer.as_asgi()),
    re_path(r"ws/post/monitor", PostMonitorConsumer.as_asgi()),
]
