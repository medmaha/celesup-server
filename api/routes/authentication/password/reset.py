from email.mime import audio
from django.http import HttpRequest
from rest_framework.generics import CreateAPIView, UpdateAPIView
from django.shortcuts import get_object_or_404

from ....library.query_param import get_query_params
from ..utils.send_mail import SendMail
from users.models import User
from django.template.loader import render_to_string
from rest_framework.response import Response

import secrets


class Request(HttpRequest):
    data: dict = {}


class ResetPassword(CreateAPIView):
    permission_classes = []
    authentication_classes = []

    def create(self, request: Request, *args, **kwargs):
        email = request.data.get("email")
        if email:
            user = get_object_or_404(User, email=email)
            auid = user.id
            stid = secrets.token_hex()

            user.secret_token = stid
            user.save()

            baseUrl = request.META["HTTP_REFERER"]
            redirect_link = baseUrl + f"auth/password/reset?auid={auid}&stid={stid}"

            template = render_to_string(
                "api/password_reset.html",
                {
                    "username": user.username.capitalize(),
                    "redirect_link": redirect_link,
                },
                request,
            )

            mail_sender = SendMail(template, email, password_reset=True)
            mail_sender.proceed()
            return Response(
                {"message": "Password reset link sended to the given mail"}, status=200
            )
        return Response({"message": "Bad request"}, status=400)


class ChangePassword(UpdateAPIView):
    permission_classes = []
    authentication_classes = []

    def update(self, request: Request, *args, **kwargs):

        query_params = get_query_params(request.get_full_path())

        auid = query_params.get("auid")
        stid = query_params.get("stid")

        if not auid or not stid:
            return Response({"message": "Account not found"}, status=404)

        user = User.objects.filter(id=auid).first()

        if user and user.secret_token == stid:
            pass
        else:
            return Response({"message": "Account not found"}, status=404)

        data: dict = request.data.copy()
        new_password = data.get("new-password")
        confirm_password = data.get("confirm-new-password")

        if not new_password or not confirm_password:
            return Response({"message": "Bad Request"}, status=400)

        new_password = new_password.strip()
        confirm_password = confirm_password.strip()

        if not new_password == confirm_password:
            return Response({"message": "Password does not match"}, status=400)

        if len(new_password) < 6:
            return Response({"message": "Password too short"}, status=400)

        user.set_password(new_password)
        user.secret_token = None
        user.save()

        return Response(
            {"message": "Your password was successfully changed", "state": "ok"},
            status=200,
        )
