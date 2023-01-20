from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

from api.routes.authentication.utils import GenerateToken, Database

from api.routes.user.serializers import UserMiniInfoSeriaLizer

from django.core.signing import dumps
from urllib.parse import urlparse


class AuthenticationTokens(TokenObtainPairView):
    """A view for getting access token and refreshing tokens"""
    authentication_classes = []

    generator_class = GenerateToken
    temporal_db = Database("signup_verification")

    def post(self, request, *args, **kwargs):

        data = request.data.copy()

        email = data.get("email") or data.get('username')
        password = data.get("password")

        user = authenticate(request, email=email, password=password)
        cookie_id = self.temporal_db.authenticate(email, password)

        if not cookie_id and not user:
            return Response(
                {"message": "Credentials do not match!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            self.serializer_class = UserMiniInfoSeriaLizer
            tokens = self.generator_class.tokens(user, self.get_serializer)
            login(request, user)
            response = Response(tokens, status=status.HTTP_200_OK)
            # response = self.create_cookie(request)
            return response

        # error
        data = {**self.temporal_db.get(cookie_id=cookie_id)}
        del data["code"]
        return Response(data, status=status.HTTP_200_OK)


    def create_cookie(self, request):
        from django.http import HttpResponse

        response = HttpResponse()
        host = request.headers.get('Origin')
        domain = urlparse(host).netloc
        # print(request.headers.get('Origin'))
        print(host, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print(domain, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        response.set_cookie('my_cookie', 'value', domain=domain, max_age=60*60*24*7)
        return response
