from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.response import Response
from rest_framework import status

from users.models import User

from api.routes.authentication.utils import GenerateToken
from api.routes.user.serializers import UserMiniInfoSeriaLizer

class RefreshAuthenticationTokens(TokenRefreshView):
    def post(self, request, *args, **kwargs):

        data = request.data.copy()
        try:
            serializer = self.get_serializer(data={"refresh": data.get('refresh')})
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(id=data["user"])

        except Exception as e:
            print('Uncaught error -->', e)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        self.serializer_class = UserMiniInfoSeriaLizer
        tokens = GenerateToken.tokens(user, self.get_serializer)
        return Response(tokens, status=status.HTTP_200_OK)

