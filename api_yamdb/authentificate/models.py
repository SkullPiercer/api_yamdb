from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=150, verbose_name='username')
    email = models.EmailField(unique=True, max_length=254, verbose_name='email')
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=(
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ), default='user')

    class Meta:
        ordering = ('email',)
