from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    is_librarian = models.BooleanField(default=False)

    def __str__(self):
        return self.username
