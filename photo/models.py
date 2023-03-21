import os
from django.db import models


class Photo(models.Model):
    USED_FOR = [
        ("post", "Post"),
        ("avatar", "Avatar"),
        ("thumbnail", "Thumbnail"),
    ]
    used_for = models.CharField(max_length=100, default="avatar", choices=USED_FOR)

    author_id = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="author"
    )
    alt_text = models.CharField(max_length=50, default="post by")
    name = models.CharField(max_length=50, default="", null=True)

    width = models.IntegerField(default=120)
    height = models.IntegerField(default=120)

    file_url = models.CharField(
        max_length=50, default=os.environ.get("DEFAULT_AVATAR_PROFILE")
    )

    def __str__(self) -> str:
        return self.alt_text

    @property
    def url(self):
        return self.file_url

    @property
    def serialized_data(self):
        return {
            "url": self.url,
            "width": self.width,
            "height": self.height,
            "alt:text": self.alt_text,
        }

    def get_serialized_data(self):
        return self.serialized_data
