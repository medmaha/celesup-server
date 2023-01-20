from rest_framework.serializers import ModelSerializer
from hashtags.models import HashTag


class HashTagDetailSerializer(ModelSerializer):
    class Meta:
        model = HashTag
        fields = ["id", "tag_text"]
