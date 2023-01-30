from urllib import response
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from django.contrib.auth import login
from rest_framework import status

from ..utils.temporal_db import Database
from ..utils.send_mail import SendMail
from django.template.loader import render_to_string

from users.models import User

from datetime import datetime, timedelta


class VerifyUserAccount(GenericAPIView):
    authentication_classes = []
    permission_classes = []

    validation_database = Database()

    def get(self, request, *args, **kwargs):
        auth_cookie = request.COOKIES.get("cs-auth")

        if not auth_cookie:
            return Response({"message": "unauthorized"}, status=HTTP_401_UNAUTHORIZED)

        db_lookup = {"key": "cookie_id", "value": auth_cookie}

        if self.validation_database.exists(db_lookup):
            auth_user_data = self.validation_database.retrieve(db_lookup, raw=True)

            if not auth_user_data.get("mailed"):
                if auth_user_data.get("email"):

                    email_address = auth_user_data["email"]
                    verification_code = self.validation_database.get_verification_code()
                    content = render_to_string(
                        "api/template_email.html",
                        {
                            "username": auth_user_data.get("username").capitalize(),
                            "code": f"C-{verification_code}",
                        },
                    )

                    mail_sender = SendMail(content, email_address, verify_email=True)
                    # mail_sender.proceed()
                    self.validation_database.update(
                        "code", verification_code, db_lookup
                    )
                    self.validation_database.update("mailed", int(True), db_lookup)

                else:
                    # Todo
                    "Phone number specified"
                    pass

            user = self.validation_database.retrieve(db_lookup, raw=True)

            data = {"username": user["username"], "id": user["id"]}

            response = Response(data, status=HTTP_200_OK)

            new_cookie = self.validation_database.create_cookie()
            self.validation_database.update("cookie_id", new_cookie, db_lookup)

            expires_at = datetime.now() + timedelta(minutes=15)
            response.set_cookie(
                "cs-auth", new_cookie, expires=expires_at, httponly=True
            )
            response.set_cookie("cs-auth-val", new_cookie, expires=expires_at)

            return response

        return Response({"message": "unauthorized"}, status=HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        auth_cookie = request.COOKIES.get("cs-auth")
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
                login(request, user)

                response = Response(
                    {
                        "message": "Ahoy {} Your account is successfully verified".format(
                            user.username.capitalize()
                        ),
                        "data": {"id": user.id},
                    }
                )
                response.delete_cookie("cs-auth")
                response.delete_cookie("cs-auth-val")

                self.validation_database.delete(db_lookup)
                return response

            elif not valid_cookie:
                response_401.delete_cookie("auth")
                return response_401
            else:
                response_400.set_cookie(
                    "cs-auth", auth_cookie, expires=expires_at_400, httponly=True
                )
                return response_400

        elif not auth_cookie:
            response_401.delete_cookie("cs-auth")
            return response_401

        else:
            response_400.set_cookie(
                "cs-auth", auth_cookie, expires=expires_at_400, httponly=True
            )
            return response_400

    def put(self, request, *args, **kwargs):
        auth_cookie = request.COOKIES.get("cs-auth")

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
