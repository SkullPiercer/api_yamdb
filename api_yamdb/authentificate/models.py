from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Модель кастомного администратора."""

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('email не может быть пуст!')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    """Модель кастомного пользователя."""
    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = (
        (ROLE_USER, 'User'),
        (ROLE_MODERATOR, 'Moderator'),
        (ROLE_ADMIN, 'Admin'),
    )
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='username'
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email'
    )
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='user'
    )

    objects = CustomUserManager()

    class Meta:
        ordering = ('email',)

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN
