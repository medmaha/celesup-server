from utilities.generators import id_generator
from django.db import models


from users.models import User

from django.db import models
from django.db.models import Q

from photo.models import Photo


MAX_FILE_SIZE = 10485760  # mega bytes


class ObjectManager(models.Manager):
    def trending(self, limit=5):
        queryset = self.filter(activity_rate__gte=3)[:limit]
        return queryset

    def not_trending(self, limit=5):
        queryset = self.filter(activity_rate__lte=3)[:limit]
        return queryset

    def get_latest(self, limit=5):
        queryset = self.filter().order_by("-created_at")[:limit]
        return queryset

    def get_earliest(self, limit=5):
        queryset = self.filter().order_by("created_at")[:limit]
        return queryset

    def smart_query(self, limit=5):
        queryset = self.filter(Q(activity_rate__gte=1))
        return queryset


class Post(models.Model):
    # id = models.CharField(max_length=100, primary_key=True, blank=True)
    key = models.CharField(max_length=100, primary_key=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author", blank=True
    )

    tags = models.ManyToManyField(User, related_name="tag", blank=True)
    publish = models.CharField(max_length=35, default="Public")

    caption = models.CharField(max_length=250, null=True, blank=True, default="")
    excerpt = models.TextField(max_length=2000, null=True, blank=True, default="")
    hashtags = models.CharField(max_length=250, null=True, blank=True, default="")

    picture = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.SET_NULL)

    likes = models.ManyToManyField(User, blank=True, related_name="post_likes")
    shares = models.ManyToManyField(User, blank=True, related_name="post_shares")
    views = models.ManyToManyField(User, blank=True, related_name="views")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    activity_rate = models.BigIntegerField(default=1, null=True, blank=True)
    objects = ObjectManager()

    child = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)

    # @property
    # def key(self):
    #     return self.id

    def __str__(self):
        return "@ " + self.author.username + f" {self.key}"

    class Meta:
        get_latest_by = "created_at"
        ordering = ("-updated_at", "activity_rate", "-created_at")

    # def save(self, *args, **kwargs):
    #     if self.id:
    #         return super().save(*args, **kwargs)

    #     id = id_generator(f"Post")
    #     self.id = id
    #     return super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.key:
            return super().save(*args, **kwargs)

        id, save_id = id_generator()
        self.key = id
        post = super().save(*args, **kwargs)
        save_id(
            f"Post {self.caption[:7] or self.excerpt[:7] or self.hashtags[:7]} @"
            + self.author.username
        )
        return post
