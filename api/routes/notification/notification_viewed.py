from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from notification.serializer import Notification
from .serializers import NotificationUpdateSerializer

from django.shortcuts import get_object_or_404


class NotificationViewed(UpdateAPIView):

    serializer_class = NotificationUpdateSerializer

    def update(self, request, *args, **kwargs):
        notification_pk = request.data.get("notification-pk")
        notification = get_object_or_404(Notification, pk=notification_pk)

        serializer = self.get_serializer(
            instance=notification, data={"is_viewed": True}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)
