from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.abstractmodels import CategoryGenre

User = get_user_model()


class Category(CategoryGenre):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'
        ordering = ('name',)


class Genre(CategoryGenre):
    """Модель жанра."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'
        ordering = ('name',)


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Максимально допустимое число символов - 256.'
    )
    year = models.IntegerField(
        max_length=4,
        verbose_name='Год создания',
        help_text='Допустимы только числа, не более 4-х.'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр произведения',
        related_name='titles',
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Промежуточная модель для жанров и произведений."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель отзыва."""

    text = models.TextField(max_length=1000, verbose_name='Текст')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(10.0), MinValueValidator(1.0)
        ]
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews_by_title', verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews_by_author', verbose_name='Автор',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('title',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='only_one_review_per_user_is_allowed'
            )
        ]


class Comment(models.Model):
    """Модель комментария."""

    text = models.TextField(max_length=1000, verbose_name='Текст')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='comments_by_title', verbose_name='Произведение',
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments_by_review', verbose_name='Комментарий'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments_by_author', verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('title',)
