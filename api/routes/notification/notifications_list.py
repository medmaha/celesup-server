from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from users.models import User
from users.serializers import UserViewSerializer
from notification.models import Notification

from .serializers import NotificationSerializer


class NotificationList(ListAPIView):
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        new_notifications = Notification.objects.filter(
            recipient=request.user, is_viewed=False
        )
        old_notifications = Notification.objects.filter(
            recipient=request.user, is_viewed=True
        )[:3]

        new_serializer = NotificationSerializer(new_notifications, many=True)
        old_serializer = NotificationSerializer(old_notifications, many=True)

        self.serializer_class = UserViewSerializer

        for data in new_serializer.data:
            if data.get("sender"):
                sender = User.objects.get(id=data["sender"])
                data["sender"] = self.get_serializer(sender).data

        for data in old_serializer.data:
            if data.get("sender"):
                sender = User.objects.get(id=data["sender"])
                data["sender"] = self.get_serializer(sender).data

        response = {"new": new_serializer.data, "old": old_serializer.data}

        return Response(response)
