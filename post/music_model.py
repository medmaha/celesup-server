from utilities.media_paths import *
from django.db import models

from django.db import models

from .utils import validate_file



def post_video_path(instance, filename):
    return f"posts/by__{instance.author.email}/videos/{filename}"


class Music(models.Model):
    audio = models.FileField(
        upload_to=post_video_path,
        validators=[validate_file],
    )
    pass
