from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class CelesupAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authenticators = [CelesupClientApi(), SessionAuthentication()]
        for authenticator in authenticators:
            user, auth = authenticator.authenticate(request) or (None, None)
            if user is not None:
                return user, auth
            else:
                break


class CelesupClientApi(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('celesup-api')
        if auth_header:
            auth_header = auth_header.split()
            try:
                if ''.join( auth_header[0].lower())+';avs' == self.authenticate_header(request):
                    # Get the session-based user from the underlying HttpRequest object
                    user = getattr(request._request, 'user', None)

                    # Unauthenticated, CSRF validation not required
                    if not user or not user.is_active:
                        return None

                    return (user, None)
            except:
                return None
          

    def authenticate_header(self, request):
        return '1.2.2v;avs'
