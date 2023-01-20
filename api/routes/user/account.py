from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import (
    UserEditSerializer,
    UserDetailSerializer,
    UserMETADATASeriaLizer,
)


class AccountSettings(GenericAPIView):

    serializer_class = UserMETADATASeriaLizer

    def get(self, request, *args, **kwargs):
        if not isinstance(request.user, User):
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        serializer = self.get_serializer(user)
        data = {**serializer.data, "emails": user.emails}
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if not isinstance(request.user, User):
            return Response(status=status.HTTP_404_NOT_FOUND)

        user: User = request.user
        data = request.data.copy()

        if "public_email" in data and user.email_privacy:
            return Response("email privacy is active", status=status.HTTP_403_FORBIDDEN)

        self.serializer_class = UserEditSerializer

        serializer = self.get_serializer(instance=user, data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        serializer = self.get_serializer(user)
        data = {**serializer.data, "emails": user.emails}
        return Response(data, status=status.HTTP_200_OK)
