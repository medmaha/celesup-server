from datetime import datetime, timedelta
import os
import uuid
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

from ..utils.tokens import GenerateToken

from api.routes.authentication.utils import Database

from users.serializers import UserViewSerializer

from users.models import User

import re
import random


class AuthenticateUser(TokenObtainPairView):
    """A view for getting access token and refreshing tokens"""

    authentication_classes = []
    permission_classes = []

    jwt_token_generator = GenerateToken()
    validation_database = Database()

    def post(self, request, *args, **kwargs):

        data = request.data.copy()

        email = data.get("email") or data.get("username") or data.get("phone", "")
        password = data.get("current-password")

        pattern = "@guest.com"

        guestUser = re.search(pattern, email)

        if guestUser:
            user, _ = User.objects.get_or_create(email=email)

            if not user.username:
                prefix = random.randrange(50, 1000)
                user.username = email.split("@")[0] + f"-{prefix}"
            if not user.password:
                user.set_password(password)
        else:
            user = authenticate(request, email=email, password=password)

        if user:
            self.serializer_class = UserViewSerializer
            tokens = self.jwt_token_generator.tokens(
                user, self.get_serializer, context={"request": request}
            )
            response = Response({"tokens": tokens}, status=status.HTTP_200_OK)
            return response

        _user = self.validation_database.authenticate(email, password)
        if _user:
            data = {
                "id": _user["id"],
                "name": _user["name"],
                "avatar": User().avatar,
                "username": _user["username"],
                "cover_img": User().cover_img,
            }
            response = Response(data, status=status.HTTP_200_OK)
            return response

        response = Response(
            {"message": "Credentials not found!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

        return response
