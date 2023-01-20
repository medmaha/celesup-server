from rest_framework.generics import ListAPIView
from rest_framework.response import Response


from messenging.models import Thread
from django.db.models import Q
from .serializers import ThreadSerializer
from ..user.serializers import UserMiniInfoSeriaLizer
from users.models import User


class ThreadList(ListAPIView):
    def get_queryset(self):
        user = self.request.user

        queryset = Thread.objects.filter(Q(recipient_id=user.id) | Q(sender_id=user.id))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = ThreadSerializer(page, many=True)
            data = self.get_data(serializer)
            return self.get_paginated_response(data)

        serializer = ThreadSerializer(queryset, many=True)
        data = self.get_data(serializer)
        return Response(data)

    def get_data(self, serializer):
        for data in serializer.data:
            self.serializer_class = UserMiniInfoSeriaLizer
            data["sender"] = self.get_serializer(
                User.objects.get(id=data["sender"])
            ).data
            data["recipient"] = self.get_serializer(
                User.objects.get(id=data["recipient"])
            ).data
            data["author"] = self.get_serializer(
                User.objects.get(id=data["author"])
            ).data
        return serializer.data
