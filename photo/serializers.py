from rest_framework import serializers

from .models import Photo


class PostViewSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    width = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = [
            "url",
            "alt_text",
            "width",
            "height",
        ]

    def get_url(self, obj):
        return obj.picture.url

    def get_width(self, obj):
        return str(obj.picture.width)

    def get_height(self, obj):
        return str(obj.picture.height)
