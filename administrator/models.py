from django.db import models
from users.models import User


class Administrator(models.Model):
    id = models.CharField(max_length=100, primary_key=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_type = models.CharField(
        max_length=50, default="Administrator", editable=False
    )

    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
