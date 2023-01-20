from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView, GenericAPIView
from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import (
    UserEditSerializer,
    UserDetailSerializer,
    UserMETADATASeriaLizer,
)
from utilities.generators import get_profile_data


class ProfileEdit(UpdateAPIView):
    serializer_class = UserEditSerializer

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.data.get("profileId"))

        data = request.data.copy()

        for field in data:
            if not data[field]:
                del data[field]

        # ? setter
        serializer = self.get_serializer(instance=user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        files = ["avatar", "cover_img"]
        for file in files:
            if file in data:
                data[file] = serializer.data[file]

        del data["profileId"]
        del data["refreshToken"]

        return Response(data, status=status.HTTP_202_ACCEPTED)


class AccountEdit(GenericAPIView):

    serializer_class = UserMETADATASeriaLizer

    def get(self, request, *args, **kwargs):
        user = request.user

        if not isinstance(user, User):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.filter_queryset(self.get_queryset(user))

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = request.data.copy()

        return super().put(request, *args, **kwargs)
