from rest_framework import serializers
from .models import Music, Video, Picture


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist', 'file')

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'title', 'duration', 'file')
        

class PictureSerializer(serializers.ModelSerializer):
    width = serializers.IntegerField()
    height = serializers.IntegerField()

    class Meta:
        model = Picture
        fields = ('id', 'title', 'file', 'width', 'height')
