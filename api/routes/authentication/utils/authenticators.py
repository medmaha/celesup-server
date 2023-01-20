from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class MultiAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authenticators = [SessionAuthentication(), JWTAuthentication()]
        for authenticator in authenticators:
            user, auth = authenticator.authenticate(request)
            if user is not None:
                return user, auth
            else:
                break


class MyAuth(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_header = auth_header.split()
            if not auth_header[0].lower() == 'custom':
                return None
            if len(auth_header) == 1:
                msg = 'Invalid custom header. No credentials provided.'
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth_header) > 2:
                msg = 'Invalid custom header. Credentials string should not contain spaces.'
                raise exceptions.AuthenticationFailed(msg)
            return auth_header[1], None

    def authenticate_header(self, request):
        return 'custom'
