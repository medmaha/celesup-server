from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from users.models import User
from users.serializers import UsersProfileViewSerializer


class ProfileView(GenericAPIView):

    serializer_class = UsersProfileViewSerializer

    # ? Another user profile
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")

        user = get_object_or_404(User, username__iexact=username)

        serializer = self.get_serializer(user)

        return Response(serializer.data, status=200)

    # ? own profile
    def get(self, request, *args, **kwargs):
        user = request.user

        if not isinstance(user, User):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(user)

        return Response(serializer.data, status=200)
