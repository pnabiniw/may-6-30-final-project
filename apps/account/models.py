import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.commons.models import BaseModel


class User(AbstractUser):
    username = models.CharField(default=uuid.uuid4, max_length=100, blank=True, unique=True)
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    account_activated = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class UserAccountActivationKey(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_activation_keys")
    key = models.CharField(max_length=50)
