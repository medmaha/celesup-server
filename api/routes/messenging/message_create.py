from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from users.models import User

from .serializers import MessageSerializer
from messenging.models import Thread


class MessageCreate(CreateAPIView):
    def create(self, request, *args, **kwargs):

        print(request.data)

        thread = get_object_or_404(Thread, id=request.data.get("thread"))
        get_object_or_404(User, id=request.data.get("recipient"))

        data = {
            "sender": request.user.id,
            "recipient": request.data.get("recipient"),
            "body": request.data.get("body"),
        }

        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        thread.last_msg = message.body
        thread.messages.add(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
