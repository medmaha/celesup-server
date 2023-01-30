from rest_framework_simplejwt.views import TokenBlacklistView


class LogoutAuthentication(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
