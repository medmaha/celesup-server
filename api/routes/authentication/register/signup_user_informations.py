from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from users.models import User
from api.routes.user.serializers import UserCreationSerializer
from .db import Database


class SignupUserInformation(CreateAPIView):
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        if not request.data.get("code"):
            return Response(
                {"message": "Code is required, maybe you should try to signup again."},
                status=400,
            )

        temporal_database = Database(table_name="signup_verification")
        client = temporal_database.retrieve_record_for_django(
            code=request.data.get("code")
        )

        if client:

            for key, val in request.data.items():
                field = {key: val}
                if not key == "avatar":
                    field.update({key: str(val).capitalize()})

                client.update(field)

            serializer = UserCreationSerializer(data=client)
            serializer.is_valid(raise_exception=True)

            try:
                first_name, last_name = client.get("full_name").split(" ")
                first_name.capitalize()
                last_name.capitalize()
            except:
                last_name = None
                first_name = client.get("full_name").capitalize()

            try:
                user = User.objects.create_user(
                    email=client.get("email"),
                    username=client.get("username"),
                    password=client.get("password"),
                    first_name=first_name,
                    last_name=last_name,
                    user_type=client.get("user_type"),
                    gender=client.get("gender"),
                    city=client.get("city"),
                    biography=client.get("biography"),
                )

                if client.get("avatar"):
                    user.avatar = client.get("avatar")
                    user.save()
            except:
                return Response(
                    {
                        "message": "We takes action as a malicious attempt! and you might face some consequences"
                    },
                    status=201,
                )

            tokens = {}
            temporal_database.delete_record(code=client.get("code"))
            return Response(
                {"message": "Successful User created", "tokens": tokens}, status=201
            )

        return Response(
            {"message": "Invalid code, maybe you should try to signup again."},
            status=400,
        )
