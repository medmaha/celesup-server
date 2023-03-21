from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers

from .models import Photo

from django.http import HttpRequest


class PhotoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["file_url", "width", "height", "alt_text", "name"]


class PhotoViewSerializer(serializers.ModelSerializer):
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

    def get_url(self, obj: Photo):
        url = obj.file_url
        return url

    def get_width(self, obj: Photo):
        return str(obj.width)

    def get_height(self, obj: Photo):
        return str(obj.height)
