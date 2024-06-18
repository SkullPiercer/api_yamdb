from django.db import models


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(
        verbose_name="Название категории",
        max_length=256,
        db_index=True,
    )
    slug = models.SlugField(
        verbose_name="Слаг категории",
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        default_related_name = "categories"


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(
        verbose_name="Название жанра",
        max_length=256,
        db_index=True,
    )
    slug = models.SlugField(
        verbose_name="Слаг жанра",
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        default_related_name = "genres"


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название",
        help_text="Максимально допустимое число символов - 256."
    )
    year = models.IntegerField(
        max_length=4,
        verbose_name="Год создания",
        help_text="Допустимы только числа, не более 4-х."
    )
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        verbose_name="Жанр произведения",
    )
    description = models.TextField(
        verbose_name="Описание произведения",
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Промежуточная модель для жанров и произведений."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genre} {self.title}"
