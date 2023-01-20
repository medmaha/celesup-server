from notification.models import Notification
from messenging.models import Message

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GenerateToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user, serializer=False):


        t = cls.token_class.for_user(user)
        if serializer:
            token = cls.get_user_data(t, user, serializer)
        else:
            token = cls.get_user_data(t, user)
        return token

    @classmethod
    def get_user_data(cls, token, user, serializer):
        user_data = serializer(user).data
        token["user"] = {}

        token["user"]["has_alerts"] = Notification.objects.filter(
            recipient=user, is_viewed=False
        ).exists()
        token["user"]["has_message"] = Message.objects.filter(
            recipient=user, is_seen=False
        ).exists()

        for key, val in user_data.items():
            token["user"][str(key)] = val

        return token

    @classmethod
    def tokens(cls, user, serializer):
        token = cls.get_token(user, serializer)

        data = {"access": str(token.access_token), "refresh": str(token)}

        return data
