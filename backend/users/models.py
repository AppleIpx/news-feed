from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
    )

    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=100,
        blank=False,
        unique=True,
    )

    username = models.CharField(
        verbose_name="Логин",
        max_length=100,
        blank=False,
        unique=True,
    )

    first_name = models.CharField(
        verbose_name="Имя",
        max_length=100,
        blank=False
    )

    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=100,
        blank=False
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.email}"
