from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from utilities.media_paths import avatar_path, cover_img_path


class User(AbstractUser):
    "Base the user class"
    id = models.CharField(max_length=100, primary_key=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_path, default="default/avatar.png")
    email = models.EmailField(
        max_length=160,
        null=False,
        unique=True,
        blank=True,
        verbose_name="primary_email",
    )
    email_2 = models.EmailField(
        max_length=160,
        null=True,
        unique=True,
        blank=True,
    )
    email_3 = models.EmailField(
        max_length=160,
        null=True,
        unique=True,
        blank=True,
    )
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        max_length=20, null=True, blank=True, default="Unspecified"
    )
    city = models.CharField(
        max_length=100, null=True, blank=True, default="Unspecified"
    )
    biography = models.CharField(max_length=350, null=True, blank=True)
    cover_img = models.ImageField(upload_to=cover_img_path, default="default/cover.jpg")
    user_type = models.CharField(max_length=20, blank=True, default="Admin")

    friends = models.ManyToManyField("User", blank=True, related_name="user_friends")
    followers = models.ManyToManyField(
        "User", blank=True, related_name="user_followers"
    )
    following = models.ManyToManyField(
        "User", blank=True, related_name="user_following"
    )

    public_email = models.EmailField(max_length=160, null=True, blank=True)
    notification_email = models.EmailField(max_length=160, null=True, blank=True)
    email_privacy = models.BooleanField(default=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    rating = models.BigIntegerField(default=0)

    verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def profile(self):
        from admin_users.models import Admin
        from celebrity.models import Celebrity
        from supporter.models import Supporter

        user_type = self.user_type.lower()
        match user_type:
            case "celebrity":
                return Celebrity.objects.get(user=self)
            case "supporter":
                return Supporter.objects.get(user=self)
            case "admin":
                return Admin.objects.get(user=self)
            case _:
                return None

    def get_profile(self):
        return self.profile

    @property
    def full_name(self):
        return self.first_name.capitalize() + " " + self.last_name.capitalize()

    @property
    def emails(self):
        em = []
        for email in [self.email, self.email_2, self.email_3]:
            if email:
                em.append({"is_primary": email == self.email, "email": email})
        return em

    @property
    def posts_count(self):
        return self.post_set.all().count()

    @property
    def shares_count(self):
        return self.friends.all().count()

    @property
    def bookmark_count(self):
        return self.friends.all().count()

    @property
    def followers_count(self):
        return self.friends.all().count()

    @property
    def followers_count(self):
        return self.friends.all().count()

    def __str__(self):
        return self.username[:25]

    def __repr__(self):
        return self.email
