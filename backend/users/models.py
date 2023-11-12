from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

MAX_LENGTH = 150


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
    ]

    email = models.EmailField(
        'Email',
        max_length=MAX_LENGTH,
        unique=True,
    )
    username = models.CharField(
        'Юзернейм',
        max_length=MAX_LENGTH,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Недопустимый символ'
        )]
    )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH
    )
    password = models.CharField(
        'Пароль',
        max_length=MAX_LENGTH
    )
    role = models.CharField(
        'Роль пользователя',
        choices=ROLE_CHOICES,
        default=USER,
        max_length=5,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff
