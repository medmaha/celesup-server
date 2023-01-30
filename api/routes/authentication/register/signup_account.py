from rest_framework.generics import GenericAPIView
from users.models import User
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from ..utils.temporal_db import Database

from datetime import datetime, timedelta


class SignupAccount(GenericAPIView):
    authentication_classes = []
    permission_classes = []

    validation_database = Database()

    def post(self, request, *args, **kwargs):

        data: dict = request.data.copy()
        cookie_id = request.COOKIES.get("cs-auth")

        if "initial" in data:
            field, value = get_auth_field(data)
            if field:
                return self.stage_1(
                    field, value, {"key": "cookie_id", "value": cookie_id}
                )

        if "password" in data and ("email" in data and "username" in data):
            username = data["username"]
            password = validate_password(data["password"])
            auth_cookie = request.COOKIES.get("cs-auth")

            if password and auth_cookie:
                return self.stage_2(auth_cookie, username, password)

        return Response(
            {"message": "invalid credentials".capitalize()},
            status=HTTP_400_BAD_REQUEST,
        )

    def stage_1(self, field: str, value: str, cookie_lookup):
        check_existence = User.objects.filter(
            Q(email__exact=value)
            | Q(username__exact=value)
            # & Q(phone__exact=field)
        ).exists()

        if check_existence:
            response = Response(
                {"message": "email already exist", "data": {field: value}}, status=400
            )
            return response

        cookie_id = self.validation_database.insert(field, value, cookie_lookup)

        if cookie_id:
            response = Response({"message": "valid", field: value}, status=HTTP_200_OK)
            expires_at = datetime.now() + timedelta(minutes=2)
            response.set_cookie("cs-auth", cookie_id, expires=expires_at, httponly=True)
            return response

        response = Response(
            {"message": "aaaaaaaaaaaaaaaaa", "data": value}, status=HTTP_400_BAD_REQUEST
        )
        return response

    def stage_2(self, cookie: str, username: str, password: str):
        check_existence = User.objects.filter(Q(username__exact=username)).exists()

        if check_existence:
            response = Response(
                {"message": "User with this name already exist", "username": username},
                status=HTTP_400_BAD_REQUEST,
            )
            expires_at = datetime.now() + timedelta(minutes=3)
            response.set_cookie("cs-auth", cookie, expires=expires_at, httponly=True)
            return response

        query_lookup = {"key": "cookie_id", "value": cookie}
        cookie_exist = self.validation_database.exists(query_lookup)

        if not cookie_exist:
            response = Response(
                {"message": "invalid credentials"}, status=HTTP_401_UNAUTHORIZED
            )
            return response

        new_cookie_id = self.validation_database.create_cookie()
        decrypted_password = self.validation_database.encrypt_crypto_str(password)
        self.validation_database.update("username", username, query_lookup)
        self.validation_database.update("password", decrypted_password, query_lookup)
        self.validation_database.update("cookie_id", new_cookie_id, query_lookup)
        query_lookup["value"] = new_cookie_id

        user = self.validation_database.retrieve(query_lookup, raw=True)

        data = {
            "username": user["username"],
            "id": user["id"],
            "avatar": "/images/avatar.png",
        }

        response = Response(data, status=HTTP_200_OK)

        expires_at = datetime.now() + timedelta(minutes=15)
        response.set_cookie("cs-auth", new_cookie_id, expires=expires_at, httponly=True)
        response.set_cookie("cs-auth-val", new_cookie_id, expires=expires_at)
        return response


def get_auth_field(data: dict):
    allowed = ["email", "phone"]
    for field in allowed:
        if field in data and len(data.get(field)) > 2:
            return (field.strip(), data[field])


def validate_password(password: str):
    if len(password) > 6:
        return password
