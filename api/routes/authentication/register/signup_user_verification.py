from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import User
from api.routes.authentication.utils import GenerateToken
from .db import Database


class SignupUserVerification(APIView):
    "Verifies the client whose trying to register by sending a (validation code) to the givin email"
    permission_classes = []
    authentication_classes = []

    temporal_database = Database(table_name="signup_verification")

    def get(self, request, format=None):
        cookie = request.COOKIES.get("cookie_id")
        if cookie is not None and self.temporal_database.is_authenticate(cookie):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        data = request.data
        if "resend-code" in data and "email" in data:
            self.temporal_database.update_code(data["email"])

        CODE = data.get("code")

        if not CODE:
            if self.temporal_database.get_record(code=CODE):
                client = self.temporal_database.retrieve_record_for_django(code=CODE)
                user = User.objects.create_user(
                    email=client.get("email"),
                    username=client.get("username"),
                    password=client.get("password"),
                    user_type=client.get("user_type"),
                    verified=True,
                )

                tokens = GenerateToken.tokens(user)

                return Response(
                    tokens,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {"message": "Invalid Code"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": "Invalid Code"}, status=status.HTTP_400_BAD_REQUEST)
