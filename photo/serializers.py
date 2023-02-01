from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers

from .models import Photo

from django.http import HttpRequest


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

    def get_url(self, obj: Photo):
        request = self.context["request"]

        if request:
            protocol = "https://" if request.is_secure() else "http://"
            domain = get_current_site(request).domain
            url = obj.url
            return protocol + domain + url

        return obj.url

    def get_width(self, obj: Photo):
        return str(obj.width)

    def get_height(self, obj: Photo):
        return str(obj.height)
