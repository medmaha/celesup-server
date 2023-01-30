from cmath import log
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

from api.routes.authentication.utils import Database

from users.serializers import UserViewSerializer


class AuthenticateUser(TokenObtainPairView):
    """A view for getting access token and refreshing tokens"""

    authentication_classes = []
    permission_classes = []

    # jwt_token_generator = GenerateToken
    validation_database = Database()

    def post(self, request, *args, **kwargs):

        data = request.data.copy()

        email = data.get("email") or data.get("username") or data.get("phone")
        password = data.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            # tokens = self.jwt_token_generator.tokens(user,  self.get_serializer)

            login(request, user)

            self.serializer_class = UserViewSerializer
            serializer = self.get_serializer(user)
            response = Response(serializer.data, status=status.HTTP_200_OK)
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

            # Todo secure the cookies on production
            expires_at = datetime.now() + timedelta(minutes=15)
            response.set_cookie("cs-auth", cookie_id, expires=expires_at, httponly=True)
            response.set_cookie("cs-auth-val", cookie_id, expires=expires_at)
            return response

        response = Response(
            {"message": "Credentials do not match!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        response.delete_cookie("cs-auth")
        response.delete_cookie("cs-auth-val")
        return response
