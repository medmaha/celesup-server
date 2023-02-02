from rest_framework.authentication import BaseAuthentication
from users.models import User


class CelesupClientApi(BaseAuthentication):
    def __init__(self) -> None:
        super().__init__()
        self.name = "CELESUP AUTH"

    def authenticate(self, request):
        auth_header: str = request.headers.get("celesup-api")

        if auth_header:
            auth_header, user_id = auth_header.split("||")
            try:
                if "".join(auth_header.lower()) + ";avs" == self.authenticate_header(
                    request
                ):
                    # Get the session-based user from the underlying HttpRequest object
                    user = User.objects.get(pk=user_id)

                    # Unauthenticated, CSRF validation not required
                    if not user.is_active:
                        return None, None

                    return (user, auth_header)
            except:
                return None, None
        return None, None

    def authenticate_header(self, request):
        return "1.2.2v;avs"
