from users.models import User
from utilities.media_paths import *

from PIL import Image

from django.db import models

from utilities.resize_image import responsive_resize
from .utils import validate_file


def post_photo_path(instance, filename):
    return f"posts/by__{instance.author.email}/photos/{filename}"


class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.FileField(
        upload_to=post_photo_path,
        default="default/photo.png",
        null=True,
        blank=True,
        # validators=[validate_file],
    )

    alt_text = models.CharField(max_length=50, default="post by")

    def __str__(self) -> str:
        return self.image.url

    @property
    def get_size(self):
        "Returns a tuple with the width and height"
        image = Image.open(self.image.path)
        return image.size

    @property
    def width(self):
        return self.get_size[0]

    @property
    def height(self):
        return self.get_size[1]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        responsive_resize(self.image.path)
