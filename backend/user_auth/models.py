import datetime
from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


def get_token_expire_time():
    return timezone.now() + datetime.timedelta(minutes=15)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class PasswordReset(models.Model):
    token = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid4)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    expire_time = models.DateTimeField(
        default=get_token_expire_time, editable=False)
