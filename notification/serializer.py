from rest_framework.serializers import ModelSerializer
from .models import Notification

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['pk', 'sender', 'recipient', 'hint', 'content', 'is_viewed', 'created_at']
