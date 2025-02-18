from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=100, verbose_name='имя')
    email = models.EmailField(unique=True, verbose_name='email')
    password = models.CharField(max_length=100, **NULLABLE, verbose_name='пароль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('pk',)
