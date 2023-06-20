from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = first_name = models.CharField(
        _("first name"),
        max_length=150,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
    )
    password = models.CharField(
        _("password"),
        max_length=150,
    )

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    @property
    def is_admin(self):
        return self.is_staff
