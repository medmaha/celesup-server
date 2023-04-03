from django.db import models
from django.contrib.auth.models import AbstractUser

import os


class User(AbstractUser):
    "Base the user class"

    GENDER = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    ACCOUNT_TYPES = [
        ("celesup", "Celesup"),
        ("support", "Supporter"),
        ("administrator", "Administrator"),
    ]

    id = models.CharField(max_length=100, primary_key=True, blank=True, unique=True)

    avatar = models.CharField(max_length=300, default="/images/default-avatar.png")
    cover_img = models.CharField(
        max_length=300, default="/images/default-cover_img.png"
    )

    email = models.EmailField(max_length=160, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)
    secret_token = models.CharField(max_length=160, null=True, blank=True)

    city = models.CharField(null=True, blank=True, max_length=150)
    biography = models.CharField(max_length=350, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True, choices=GENDER)

    account_type = models.CharField(max_length=20, blank=True, choices=ACCOUNT_TYPES)

    email_privacy = models.BooleanField(default=True, blank=True)
    public_email = models.CharField(max_length=160, null=True, blank=True)
    notification_email = models.CharField(max_length=20, blank=True, null=True)
    secondary_email = models.EmailField(
        max_length=160, unique=True, blank=True, null=True
    )

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    account_rating = models.BigIntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "account_type"]

    @property
    def full_name(self):
        if self.name:
            return self.name.capitalize() + " " + self.last_name.capitalize()
        return ""

    @property
    def emails(self):
        em = []
        for email in [self.email, self.secondary_email]:
            if email:
                em.append({"is_primary": email == self.email, "email": email.text})
        return em

    def __str__(self):
        return self.username[:25]

    def __repr__(self):
        return self.email
