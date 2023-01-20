from users.models import User
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import UserDetailSerializer

class UserProfiles(ListAPIView):

    def list(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response({"users": serializer.data})