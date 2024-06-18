from django.db import models


class CategoryGenre(models.Model):
    """Абстрактная модель для Category и Genre."""
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        db_index=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=50,
        unique=True,
    )
