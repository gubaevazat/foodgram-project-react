from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = first_name = models.CharField(
        max_length=150,
        verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='электронная почта'
    )

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.get_full_name()
