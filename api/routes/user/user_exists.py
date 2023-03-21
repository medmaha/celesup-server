from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework import status

from users.models import User


class UserExists(RetrieveAPIView):
    permission_classes = []
    authentication_classes = []

    def retrieve(self, request: HttpRequest, *args, **kwargs):

        split_url = request.get_full_path().split("?")

        try:
            query = split_url[1]
            key, value = query.split("=")
            if key == "auid":
                user = User.objects.filter(id=value)
                if user.first():
                    return Response({"exists": True}, status=status.HTTP_200_OK)
                return Response(status=status.HTTP_200_OK)
            else:
                raise ValueError()

        except:
            return Response(
                {"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST
            )
