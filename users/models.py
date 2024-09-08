from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя
    """
    username = None

    email = models.EmailField(
        max_length=50,
        verbose_name='Email',
        unique=True,
    )
    telephone = models.PositiveIntegerField(
        verbose_name="Номер телефона"
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/",
        verbose_name="Аватар",
        blank=True,
        null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ('id',)

    def __str__(self):
        return self.email