from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOISES = (
    ('user', 'user'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    """Кастомная модель юзера"""
    email = models.EmailField(
        'Электронная почта',
        blank=False, null=False,
        unique=True, max_length=254
    )
    password = models.CharField(
        'Пароль',
        blank=False, null=False,
        unique=True, max_length=128
    )
    username = models.CharField(
        'Юзернэйм',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        blank=True, null=True,
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        blank=True, null=True,
        max_length=150
    )
    role = models.CharField(
        choices=ROLE_CHOISES, default='user',
        max_length=9
    )

    REQUIRED_FIELDS = [
        'email',
        'username',
        'password',
        'first_name',
        'last_name'
    ]

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            )
        ]

    def __str__(self):
        return self.username
