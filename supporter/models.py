""" A sub_user categories"""

from django.db import models
from users.models import User


class Supporter(models.Model):
    id = models.CharField(max_length=100, primary_key=True, blank=True)
    user = models.OneToOneField(User, models.CASCADE, related_name="supporter_user")
    profile_type = models.CharField(
        max_length=50, blank=True, default="Supporter", editable=False
    )
