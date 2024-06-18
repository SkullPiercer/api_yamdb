from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    role = models.CharField(max_length=50, choices=(
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ), default='user')
