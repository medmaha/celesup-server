from PIL import Image

from django.db import models


def post_photo_path(instance, filename):
    return f"{instance.used_for}/by__{instance.author_id}/photos/{filename}"


class Photo(models.Model):
    USED_FOR = [
        ("post", "Post"),
        ("avatar", "Avatar"),
        ("thumbnail", "Thumbnail"),
    ]

    author_id = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="author"
    )
    alt_text = models.CharField(max_length=50, default="post by")
    used_for = models.CharField(max_length=100, default="avatar", choices=USED_FOR)
    file = models.FileField(
        upload_to=post_photo_path,
        default="default/avatar.png",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.file.name

    @property
    def get_size(self):
        "Returns a tuple with the width and height"
        image = Image.open(self.file.path)
        return image.size

    @property
    def url(self):
        return self.file.url

    @property
    def width(self):
        return self.get_size[0]

    @property
    def height(self):
        return self.get_size[1]

    @property
    def data(self):
        return {
            "url": self.url,
            "width": self.width,
            "height": self.__height,
            "alt:text": self.alt_text,
        }
