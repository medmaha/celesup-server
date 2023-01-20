from utilities.media_paths import *
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class HashTag(models.Model):
    id = models.CharField(max_length=100, primary_key=True, blank=True)
    avatar = models.ImageField(
        upload_to=avatar_path, default="profiles/avatar_default.png"
    )
    tag_text = models.CharField(max_length=100)
    tag_symbol = models.CharField(max_length=1, default="#")

    object_id = models.CharField(max_length=255)
    object = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
