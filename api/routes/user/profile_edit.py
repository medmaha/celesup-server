from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from django.shortcuts import get_object_or_404
from users.models import User
from users.serializers import UsersProfileViewSerializer, UserProfileUpdateSerializer

from api.routes.authentication.utils.tokens import GenerateToken


class ProfileEdit(UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer

    token_generator = GenerateToken()

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.data.get("profileId"))

        if user != request.user:
            return Response(
                {"message": "unauthorized"}, status=status.HTTP_403_FORBIDDEN
            )

        data: dict = request.data.copy()

        # delete empty values
        for field in data.copy().keys():
            if not data[field]:
                del data[field]
            if field == "gender":
                data["gender"] = data["gender"].lower()

        # ? setter
        serializer = self.get_serializer(instance=user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(id=user.id)

        self.serializer_class = UsersProfileViewSerializer

        tokens = self.token_generator.tokens(
            user, self.get_serializer, context={"request": request}
        )

        serializer = self.get_serializer(user, context={"request": request})

        return Response(
            {"user": serializer.data, "tokens": tokens}, status=status.HTTP_200_OK
        )
