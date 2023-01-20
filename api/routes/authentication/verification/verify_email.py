from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import User
from api.routes.authentication.utils import GenerateToken, Database, SendMail
from django.template.loader import render_to_string


class VerifyEmailAddress(APIView):
    "Verifies the client whose trying to register by sending a (validation code) to the givin email"
    permission_classes = []
    authentication_classes = []

    temporal_db = Database(table_name="signup_verification")

    def get(self, request, format=None):

        auth_cookie = request.headers.get("Authorization")
        cookie = self.is_cookie_authorized(auth_cookie)

        if not cookie:
            return self.missing_cookie_response()

        is_authenticated = self.temporal_db.is_authenticated(cookie)

        if is_authenticated:

            user = self.temporal_db.get(cookie_id=cookie)
            if not user["mailed"]:
                recipient = user["email"]
                content = render_to_string(
                    "template_email.html",
                    {"code": user["code"], "username": user["username"]},
                )
                mail = SendMail(content, recipient, verify_email=True)
                mail.proceed()
                self.temporal_db.update("mailed", int(True), ("cookie_id", cookie))

            return Response(status=status.HTTP_200_OK)

        return self.missing_cookie_response()

    def post(self, request, format=None):

        auth_cookie = request.headers.get("Authorization")
        COOKIE = self.is_cookie_authorized(auth_cookie)

        if not COOKIE:
            return self.missing_cookie_response()

        self.cookie = COOKIE
        user = self.temporal_db.get(cookie_id=COOKIE)

        if "logout-cookie" in request.data and user:
            return self.logout_cookie()

        if "resend-code" in request.data and user:
            return self.resend_verification_code(user)

        VERIFICATION_CODE = request.data.get("code")

        if self.temporal_db.exists(code=f"C-{VERIFICATION_CODE}"):
            client = self.temporal_db.get_raw_data(cookie_id=self.cookie)

            user = User.objects.create_user(
                email=client["email"],
                username=client["username"],
                password=client["password"],
                user_type=client["user_type"],
                verified=True,
            )

            tokens = GenerateToken.tokens(user)
            self.temporal_db.delete(code=VERIFICATION_CODE)
            return Response(
                tokens,
                status=status.HTTP_201_CREATED,
            )

        data = {"message": "Code is required"}

        if VERIFICATION_CODE:
            data["message"] = "Invalid code"

        return Response(
            data,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, format=None):

        auth_cookie = request.headers.get("Authorization")
        cookie = self.is_cookie_authorized(auth_cookie)

        if not cookie:
            return self.missing_cookie_response()

        if self.temporal_db.is_authenticated(cookie):
            pass

    def logout_cookie(self):
        self.temporal_db.update("is_logged_in", int(False), ("cookie_id", self.cookie))
        return Response(status=status.HTTP_200_OK)

    def resend_verification_code(self, user):
        code = self.temporal_db.update_code(cookie_id=self.cookie)

        recipient = user["email"]
        content = render_to_string(
            "template_email.html",
            {"code": code, "username": user["username"]},
        )

        mail = SendMail(content, recipient, verify_email=True)
        # mail.proceed()
        data = {"message": "Sending code! this could take a minute"}

        return Response(data, status=status.HTTP_200_OK)

    def missing_cookie_response(self):
        return Response(
            {"message": "Code is missing or invalid"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def is_cookie_authorized(self, cookie=""):
        if not cookie:
            return False

        try:
            auth, cid = cookie.split(" ")
            if auth in ("Celesup", "JWT"):
                return cid
            return False
        except:
            return False
