from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Менеджер пользователя, где email — уникальный идентификатор."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    ]

    username = None
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', unique=True)
    role = models.CharField('Роль', max_length=10, choices=ROLE_CHOICES, default='user')
    image = models.ImageField('Аватар', upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
