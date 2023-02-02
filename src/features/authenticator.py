import os

from rest_framework.authentication import BaseAuthentication
from .jwt_auth import JWTAuthentication
from .session_auth import SessionAuthentication
from .celesup_auth import CelesupClientApi

AUTH_MECHANISM = os.environ.get("AUTHENTICATION_MECHANISM")


class CelesupAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authenticators = [CelesupClientApi()]
        match AUTH_MECHANISM:
            case "JWT":
                authenticators.append(JWTAuthentication())
            case "SESSION":
                authenticators.append(SessionAuthentication())

        for idx, authenticator in enumerate(authenticators):
            user, auth = authenticator.authenticate(request)

            if user is not None:
                if idx < (len(authenticators) - 1):
                    continue
                return user, auth
            else:
                break

        return None, None
