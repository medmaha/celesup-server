from django.db import models
from post.models import Post
from users.models import User

from utilities.media_paths import comment_picture_path, comment_file_path


class Comment(models.Model):
    post = models.ForeignKey(
        Post, null=True, blank=True, related_name="comment", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, blank=True, related_name="comment_author", on_delete=models.CASCADE
    )
    content = models.TextField(max_length=1000)
    file = models.FileField(null=True, blank=True, upload_to=comment_file_path)
    picture = models.ImageField(null=True, blank=True, upload_to=comment_picture_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )
    likes = models.ManyToManyField(User, blank=True)
    is_updated = models.BooleanField(default=False)
    activity_rate = models.BigIntegerField(default=1, null=True, blank=True)


    def __str__(self):
        return f"{self.author.username}/{self.content[:15]}..."

    def get_replies(self, max=15):
        replies = Comment.objects.filter(post_id=self.post.key, parent_id=self.id)[:max]

        return replies

    class Meta:
        ordering = ("-updated_at", "activity_rate", "-created_at")
