from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields["is_active"] = True
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
    )
    username = models.CharField(
        max_length=150,
    )
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} {self.email}"
