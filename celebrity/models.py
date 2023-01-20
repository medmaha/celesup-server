""" a sub user category"""

from django.db import models
from users.models import User
from post.models import Post

# class FanClub(models.Model):
#     """
#     Provides a fan base functionality for a celebrity user...
#     * One fans club for each celebrity
#     """
#     name = models.CharField(max_length=100)
#     members = models.ManyToManyField(User, blank=True)
#     conversations = [{
#         'author':'medmaha',
#         'message':'my fav! i love j-hus',
#     }]


class Celebrity(models.Model):
    """
    Celebrity user account class
    """

    id = models.CharField(max_length=100, unique=True, primary_key=True)
    user = models.OneToOneField(User, models.CASCADE, related_name="celebrity_user")
    friends = models.ManyToManyField(User, blank=True, related_name="celebrity_friends")
    profile_type = models.CharField(max_length=50, default="Celebrity", editable=False)

    # fan_club  = models.OneToOneField(FanClub, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = "Celebrity"
        verbose_name_plural = "Celebrities"
