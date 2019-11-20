import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .helpers import SingletonModel


class User(AbstractUser):
    pass


class Congregation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Setting(SingletonModel):
    initial_data_runned = models.BooleanField(default=False, blank=True)
