from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if value > 10:
            raise serializers.ValidationError('Выше 10 баллов низя!')
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method == "POST":
            title = get_object_or_404(
                Title, id=self.context.get('view').kwargs.get('title_id')
            )
            if Review.objects.filter(
                author=request.user, title=title
            ).exists():
                raise serializers.ValidationError(
                    'Возможно добавить только 1 отзыв к 1 произведению!'
                )
        return attrs
