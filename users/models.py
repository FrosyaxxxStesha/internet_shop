from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='почта',
        unique=True
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="users/avatars/",
        default="users/avatars/default/default.svg"
    )
    telephone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        unique=True,
        null=True,
        blank=True
    )
    country = models.CharField(
        max_length=30,
        verbose_name="Страна",
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
