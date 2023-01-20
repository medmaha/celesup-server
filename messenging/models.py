from django.db import models
from users.models import User


class Message(models.Model):
    id = models.CharField(max_length=100, primary_key=True, blank=True)

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="msg_sender",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="msg_recipient",
    )

    body = models.TextField(max_length=1000)
    delivered = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Thread(models.Model):
    id = models.CharField(max_length=100, primary_key=True, blank=True)
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="thread_sender",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="thread_recipient",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="thread_author",
    )
    last_msg = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
    )
    last_msg_date = models.DateTimeField(auto_now=True)
    messages = models.ManyToManyField(Message, blank=True)
