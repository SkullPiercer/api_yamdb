from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Category, Comment, Genre, Review, Title,
    MIN_SCORE_VALUE, MAX_SCORE_VALUE
)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    def validate(self, attrs):
        kwargs = self.context.get('view').kwargs
        request = self.context.get('request')
        if request.method == 'POST':
            get_object_or_404(
                Title, id=kwargs.get('title_id')
            )
            get_object_or_404(
                Review, id=kwargs.get('review_id')
            )
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(
        min_value=MIN_SCORE_VALUE,
        max_value=MAX_SCORE_VALUE
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method == 'POST':
            title = get_object_or_404(
                Title, id=self.context['view'].kwargs.get('title_id')
            )
            if request.user.reviews_by_author.filter(
                title_id=title.id
            ).exists():
                raise serializers.ValidationError(
                    'Возможно добавить только 1 отзыв к 1 произведению!'
                )
        return attrs


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели категорий."""

    class Meta:
        model = Category
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведений."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(source='rating_count')

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'genre', 'description', 'category'
        )

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения модели произведений."""

    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'genre', 'description', 'category'
        )
