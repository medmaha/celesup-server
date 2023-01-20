from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "notification alert"
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        events = {"type": "handle_recipient", "payload": data}
        async_to_sync(self.channel_layer.group_send)(self.group_name, events)

    def handle_recipient(self, events):
        data = events["payload"]
        recipient_id = data["id"]
