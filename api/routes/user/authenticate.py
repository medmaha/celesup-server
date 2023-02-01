from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from users.models import User
from post.models import Post
from utilities.generators import get_profile_data
from api.routes.user.serializers import UserMiniInfoSeriaLizer


class AuthenticateUser(GenericAPIView):

    serializer_class = UserMiniInfoSeriaLizer

    def get(self, request, *args, **kwargs):
        print(request)
        user = request.user

        if not isinstance(user, User):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=200)
