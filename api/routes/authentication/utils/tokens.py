from notification.models import Notification
from messenging.models import Message
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GenerateToken(TokenObtainPairSerializer):
    def get_token(self, user, serializer_method, **kwargs):

        t = self.token_class.for_user(user)
        token = self.get_user_data(t, user, serializer_method, **kwargs)

        return token

    def get_user_data(self, token, user, serializer_method, **kwargs):
        serialized_data = serializer_method(user, **kwargs).data

        token["user"] = {}

        token["user"]["has_notifications"] = Notification.objects.filter(
            recipient=user, is_viewed=False
        ).exists()
        token["user"]["has_messageS"] = Message.objects.filter(
            recipient=user, is_seen=False
        ).exists()

        for key, val in serialized_data.items():
            token["user"][str(key)] = val

        return token

    def tokens(self, user, serializer_method: any, **kwargs):
        user = User.objects.get(pk=user.pk)
        token = self.get_token(user, serializer_method, **kwargs)

        data = {"access": str(token.access_token), "refresh": str(token)}

        return data
