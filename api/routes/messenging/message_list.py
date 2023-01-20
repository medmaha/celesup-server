from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from users.models import User

from messenging.models import Message, Thread
from utilities.generators import get_profile_data
from .serializers import MessageSerializer
from ..user.serializers import UserMiniInfoSeriaLizer


class MessageList(ListAPIView):
    def get_queryset(self):
        thread_id = self.request.get_full_path().split("?")[1].split("=")[1]
        thread = get_object_or_404(Thread, id=thread_id)
        return thread.messages.all().order_by("created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = MessageSerializer(instance=queryset, many=True)

        for data in serializer.data:
            self.serializer_class = UserMiniInfoSeriaLizer
            sender = self.get_serializer(User.objects.get(id=data["sender"])).data
            recipient = self.get_serializer(User.objects.get(id=data["recipient"])).data

            data["sender"] = sender
            data["recipient"] = recipient

        return Response(serializer.data, status=status.HTTP_201_CREATED)
