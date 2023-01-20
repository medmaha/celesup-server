from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status

from users.models import User
from api.routes.user.serializers import UserMiniInfoSeriaLizer
from django.shortcuts import get_object_or_404

class UserInformation(GenericAPIView):
    serializer_class = UserMiniInfoSeriaLizer
    def get(self, request, id, *args, **kwargs):
        user = get_object_or_404(User, id=id)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

  
