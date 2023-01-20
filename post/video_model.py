from utilities.media_paths import *
from django.db import models


from users.models import User

from django.db import models

from .utils import validate_file


MAX_FILE_SIZE = 10485760  # mega bytes



def post_video_path(instance, filename):
    return f"posts/by__{instance.author.email}/videos/{filename}"


class Video(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(
        upload_to=post_video_path,
        null=True,
        blank=True,
        validators=[validate_file],
    )
    title = models.TextField(
        max_length=150,
        null=True,
        blank=True,
    )
    alt_text = models.CharField(max_length=50, default="post")
    thumbnail = models.ImageField(
        upload_to=post_thumbnail_path,
        default="default/video.png",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.file.url

