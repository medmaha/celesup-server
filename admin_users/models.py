from django.db import models
from users.models import User


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_type = models.CharField(max_length=50, default='Admin', editable=False)

    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


