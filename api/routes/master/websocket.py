import json
from django.urls import re_path
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from users.models import User
from messenging.models import Thread

from ..user.serializers import UserMiniInfoSeriaLizer
from .hash_table import HashTable

HASH_TABLE = HashTable()


class WSMasterConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "master"
        self.user_id = ""
        try:
            self.user_id = self.scope["query_string"].decode("utf-8").split("=")[1]
            User.objects.get(id=self.user_id)
        except:
            raise ValueError('user with id "{}" does not exist'.format(self.user_id))

        self.accept()

        HASH_TABLE[self.user_id] = {
            "CHANNEL_NAME": self.channel_name,
            "CLIENT_SOCKET": self.scope["client"],
        }

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        if data["type"] == "NOTIFY_USER":
            user_id = data["payload"].get("user_id").lower()
            event = {
                **data,
                "type": "notify_user",
            }
            if HASH_TABLE.get(user_id):
                channel = HASH_TABLE[user_id]["CHANNEL_NAME"]
                async_to_sync(self.channel_layer.send)(channel, event)
            print(HASH_TABLE[user_id])

    def notify_user(self, event):
        event = {**event, "type": "NOTIFY_USER"}
        self.send(text_data=json.dumps(event))


master_ws_urlpatterns = [
    re_path(r"ws/master", WSMasterConsumer.as_asgi()),
]
