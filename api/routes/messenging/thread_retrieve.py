from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from messenging.models import Thread, Message
from users.models import User

from .serializers import ThreadSerializer, MessageSerializer
from utilities.generators import get_profile_data
from django.shortcuts import get_list_or_404

from api.routes.user.serializers import UserMiniInfoSeriaLizer


class ThreadRetrieve(RetrieveAPIView):
    def get_queryset(self):
        recipient_id = self.request.get_full_path().split("?")[1].split("=")[1]
        user = get_object_or_404(User, id=recipient_id)

        thread = Thread.objects.filter(sender=user, recipient=self.request.user)
        if not thread.exists():
            thread = Thread.objects.filter(sender=self.request.user, recipient=user)
            if not thread.exists():
                thread = Thread.objects.create(
                    sender=self.request.user,
                    recipient=user,
                    author=self.request.user,
                )
                return thread

            return thread[0]
        return thread[0]

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        self.serializer_class = ThreadSerializer
        thread_serializer = self.get_serializer(queryset)
        data = thread_serializer.data

        self.serializer_class = UserMiniInfoSeriaLizer

        sender_serializer = self.get_serializer(User.objects.get(id=data["sender"]))
        recipient_serializer = self.get_serializer(
            User.objects.get(id=data["recipient"])
        )

        data["sender"] = sender_serializer.data
        data["recipient"] = recipient_serializer.data
        return Response(data)
