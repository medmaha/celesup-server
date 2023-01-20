from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from api.routes.user.serializers import UserCreationSerializer


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.http import HttpRequest

from ..utils import Database

from users.models import User


class Registration(APIView):
    "signup route for initial client data collection"

    permission_classes = []
    authentication_classes = []

    temporal_db = Database(table_name="signup_verification")

    def post(self, request: HttpRequest, format=None):

        serializer = UserCreationSerializer(data=request.data)
        data = request.data.copy()

        ERROR = checkError(data)
        if ERROR:
            return ERROR

        serializer.is_valid(raise_exception=True)

        db = self.temporal_db.add(
            email=data["email"],
            username=data.get("username"),
            password=data["password"],
            user_type=data.get("user_type").capitalize(),
        )
        cookie_id = self.temporal_db.authenticate(
            email=data["email"], password=data["password"]
        )

        if db is not None and cookie_id:
            _data = {
                "email": data["email"],
                "username": data["username"],
                "state": "unverified",
                "cookie_id": cookie_id,
            }
            return Response(_data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Oops something went wrong! this not your fault"},
            status=status.HTTP_400_BAD_REQUEST,
        )


def checkError(data):
    existing_email = User.objects.filter(email=data.get("email")).exists()
    existing_username = User.objects.filter(
        username__iexact=data.get("username")
    ).exists()

    if existing_email:
        return Response(
            {"message": "user with this email already exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if existing_username:
        return Response(
            {"message": "username already exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if data.get("password") and len(data.get("password")) < 6:
        return Response(
            {"message": "password this too short"},
            status=status.HTTP_400_BAD_REQUEST,
        )
