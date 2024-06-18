from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=(
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ), default='user')

    class Meta:
        ordering = ('email',)
