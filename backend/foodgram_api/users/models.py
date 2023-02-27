from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField, ManyToManyField


class User(AbstractUser):
    email = EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
        help_text='Введите адрес своей электронной почты',
    )
    username = CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        help_text='Придумайте запоминающийся, но оригинальный Логин'
    )
    first_name = CharField(
        verbose_name='Имя',
        max_length=150,
        help_text='Введите свое имя'
    )
    last_name = CharField(
        verbose_name='Фамилия',
        max_length=150,
        help_text='Введите свою фамилию'
    )
    password = CharField(
        verbose_name='Пароль',
        max_length=150,
        help_text='Введите оригинальный запоминающийся пароль'
    )
    subscribe = ManyToManyField(
        to='self',
        verbose_name='Подписка',
        related_name='subscribers',
        symmetrical=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['first_name'], name='first_name_idx'),
        ]

    def __str__(self) -> str:
        return f'{self.username}: {self.email}'
