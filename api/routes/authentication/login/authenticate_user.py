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

from api.library.cookies import CSCookie


AUTH_TYPE = os.environ.get("AUTHENTICATION_MECHANISM")


class AuthenticateUser(TokenObtainPairView):
    """A view for getting access token and refreshing tokens"""

    authentication_classes = []
    permission_classes = []

    jwt_token_generator = GenerateToken()
    validation_database = Database()

    def post(self, request, *args, **kwargs):

        data = request.data.copy()

        if request.user.is_authenticated:
            logout(request)
            return Response(status=200)

        email = data.get("email") or data.get("username") or data.get("phone")
        password = data.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            # tokens = self.jwt_token_generator.tokens(user,  self.get_serializer)

            self.serializer_class = UserViewSerializer
            match AUTH_TYPE:
                case "JWT":
                    tokens = self.jwt_token_generator.tokens(
                        user, self.get_serializer, context={"request": request}
                    )
                    response = Response({"tokens": tokens}, status=status.HTTP_200_OK)

                case "SESSION":

                    login(request, user)
                    serializer = self.get_serializer(user)
                    response = Response(serializer.data, status=status.HTTP_200_OK)
                    response.set_cookie(
                        "cs-auth_id",
                        value=str(uuid.uuid4()).replace("-", ""),
                        max_age=settings.SESSION_COOKIE_AGE,
                        secure=settings.SESSION_COOKIE_SECURE,
                        samesite=settings.SESSION_COOKIE_SAMESITE,
                    )

            return response

        _user = self.validation_database.authenticate(email, password)

        if _user:

            data = {
                "id": _user["id"],
                "avatar": "/images/avatar.png",
                "username": _user["username"],
                "name": _user["name"],
            }
            response = Response(data, status=status.HTTP_200_OK)

            cookie_id = _user["cookie_id"]

            cookies = CSCookie(response=response)
            expires_at = datetime.now() + timedelta(minutes=15)

            cookies.set("cs-auth", cookie_id, expires=expires_at, httponly=True)
            cookies.set("cs-auth-val", cookie_id, expires=expires_at)

            return response

        response = Response(
            {"message": "Credentials do not match!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        cookies = CSCookie(response=response)
        cookies.delete("cs-auth")
        cookies.delete("cs-auth-val")

        return response
