from urllib import response
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from django.contrib.auth import login
from rest_framework import status

from ..utils.tokens import GenerateToken

from ..utils.temporal_db import Database
from ..utils.send_mail import SendMail
from django.template.loader import render_to_string

from users.models import User
from users.serializers import UserViewSerializer

from datetime import datetime, timedelta

import os

AUTH_TYPE = os.environ.get("AUTHENTICATION_MECHANISM")


class VerifyUserAccount(GenericAPIView):
    authentication_classes = []
    permission_classes = []

    validation_database = Database()

    def get_cookie_id_from_req(self, cs_auth="cs-auth"):
        cookie_id = self.request.COOKIES.get(cs_auth)
        if cookie_id:
            return cookie_id

        cookie_id = self.request.headers.get(cs_auth)
        if cookie_id:
            return cookie_id

    def get(self, request, *args, **kwargs):

        auth_cookie = self.get_cookie_id_from_req()

        if not auth_cookie:
            return Response({"message": "unauthorized"}, status=HTTP_401_UNAUTHORIZED)

        db_lookup = {"key": "cookie_id", "value": auth_cookie}

        # check for user existence in temporal db storage
        if self.validation_database.exists(db_lookup):
            auth_user_data = self.validation_database.retrieve(db_lookup, raw=True)

            send_mail_callback = None
            if not auth_user_data.get("mailed"):
                if auth_user_data.get("email"):

                    email_address = auth_user_data["email"]
                    verification_code = self.validation_database.get_verification_code()
                    content = render_to_string(
                        "api/email_verification.html",
                        {
                            "username": auth_user_data.get("username").capitalize(),
                            "code": f"C-{verification_code}",
                        },
                        request,
                    )

                    mail_sender = SendMail(content, email_address, verify_email=True)
                    send_mail_callback = mail_sender.proceed
                    self.validation_database.update(
                        "code", verification_code, db_lookup
                    )
                    self.validation_database.update("mailed", int(True), db_lookup)
                else:
                    # Todo
                    "Phone number specified"
                    pass

            if send_mail_callback:
                self.validation_database.update("mailed", 1, db_lookup)
                send_mail_callback()

            new_cookie = self.validation_database.create_cookie()
            self.validation_database.update("cookie_id", new_cookie, db_lookup)

            if AUTH_TYPE == "SESSION":
                response = Response(status=HTTP_200_OK)
                expires_at = datetime.now() + timedelta(minutes=15)
                response.set_cookie(
                    "cs-auth", new_cookie, expires=expires_at, httponly=True
                )
                response.set_cookie("cs-auth-val", new_cookie, expires=expires_at)
            else:
                response = Response({"cs-auth-val": new_cookie}, status=HTTP_200_OK)
            return response

        return Response({"message": "unauthorized"}, status=HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        auth_cookie = self.get_cookie_id_from_req()
        CODE = request.data.copy().get("code")

        response_400 = Response(
            {"message": "invalid code"}, status=status.HTTP_400_BAD_REQUEST
        )
        response_401 = Response(
            {"message": "unauthorize"}, status=status.HTTP_401_UNAUTHORIZED
        )
        expires_at_400 = datetime.now() - timedelta(minutes=15)

        if auth_cookie and CODE:
            db_lookup = {"key": "cookie_id", "value": auth_cookie}
            valid_cookie = self.validation_database.exists(db_lookup)
            db_lookup = {"key": "code", "value": CODE}
            valid_code = self.validation_database.exists({**db_lookup})

            if valid_code and valid_cookie:
                client = self.validation_database.retrieve(db_lookup, raw=True)
                user = User(
                    email=client["email"],
                    username=client["username"],
                    account_type=client["account_type"] or "supporter",
                )
                user.set_password(client["password"])
                user.is_active = True
                user.save()

                response = Response(
                    {
                        "message": "Ahoy {} Your account is successfully verified".format(
                            user.username.capitalize()
                        ),
                    }
                )
                if AUTH_TYPE == "SESSION":
                    login(request, user)
                else:
                    self.serializer_class = UserViewSerializer
                    tokens = GenerateToken().tokens(
                        user, self.get_serializer, context={"request": request}
                    )
                    response.data = {
                        "message": response.data["message"],
                        "tokens": tokens,
                    }

                if AUTH_TYPE == "SESSION":
                    response.delete_cookie("cs-auth")
                    response.delete_cookie("cs-auth-val")

                self.validation_database.delete(db_lookup)
                return response

            elif not valid_cookie:
                if AUTH_TYPE == "SESSION":
                    response_401.delete_cookie("auth")
                return response_401
            else:
                if AUTH_TYPE == "SESSION":
                    response_400.set_cookie(
                        "cs-auth", auth_cookie, expires=expires_at_400, httponly=True
                    )
                return response_400

        elif not auth_cookie:
            if AUTH_TYPE == "SESSION":
                response_401.delete_cookie("cs-auth")
            return response_401

        else:
            if AUTH_TYPE == "SESSION":
                response_400.set_cookie(
                    "cs-auth", auth_cookie, expires=expires_at_400, httponly=True
                )
            return response_400

    def put(self, request, *args, **kwargs):
        auth_cookie = self.get_cookie_id_from_req()

        db_lookup = {"key": "cookie_id", "value": auth_cookie}

        NEW_CODE = self.validation_database.update_code(db_lookup)

        if NEW_CODE:
            response = Response(
                {
                    "message": "We've resend the verification code the credentials you provided"
                }
            )
            expires_at = datetime.now() + timedelta(minutes=15)
            response.set_cookie(
                "cs-auth", auth_cookie, expires=expires_at, httponly=True
            )
            response.set_cookie("cs-auth.val", auth_cookie, expires=expires_at)
            return response

        response = Response({"message": "unauthorized"}, status=HTTP_401_UNAUTHORIZED)
        response.delete_cookie("cs-auth")
        response.delete_cookie("cs-auth-val")
        return response
