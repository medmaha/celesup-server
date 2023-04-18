from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

from notification.models import Notification

from api.routes.authentication.utils.tokens import GenerateToken

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

        email: str = data.get("email") or data.get("username") or data.get("phone", "")
        password = data.get("current-password")

        pattern = "@guest.com"

        guestUser = re.search(pattern, email)

        if guestUser:
            prefix = random.randrange(50, 1000)

            user, created = User.objects.get_or_create(email=email)

            if not created:
                user = authenticate(email=email, password=password)
                if not user:
                    return Response(
                        {"message": "Wrong credentials provided"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            else:
                user.username = email.split("@")[0] + f"-{prefix}"
                user.set_password(password)

                user.save()
                alert_1 = Notification()
                alert_1.from_platform = True
                alert_1.recipient = user
                alert_1.action = "Celehub welcomes you"
                alert_1.hint_img = "/images/welcome.png"
                alert_1.save()

                alert_2 = Notification()
                alert_2.from_platform = True
                alert_2.recipient = user
                alert_2.action = (
                    "You will see both your new and old notifications here."
                )
                alert_2.hint_img = "/images/info.png"
                alert_2.save()
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
