from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from reviews.filters import TitleFilter
from reviews.mixins import GenreCategoryBaseMixin, ReviewCommentMixin
from reviews.models import Category, Genre, Review, Title
from reviews.permissions import IsAdminOrReadOnly
from reviews.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleWriteSerializer
)


class CategoryViewSet(GenreCategoryBaseMixin):
    """Просмотр, редактирование и удаление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)


class GenreViewSet(GenreCategoryBaseMixin):
    """Просмотр, редактирование и удаление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)


class ReviewViewset(ReviewCommentMixin):
    """Просмотр, редактирование и удаление отзывов."""
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(
            Title, id=self.kwargs['title_id']
        )

    def get_queryset(self):
        return self.get_title().reviews_by_title.all()

    def perform_create(self, serializer):
        serializer.save(
            title=self.get_title(), author=self.request.user
        )


class CommentViewset(ReviewCommentMixin):
    """Просмотр, редактирование и удаление комментариев."""
    serializer_class = CommentSerializer

    def get_review(self):
        return Review.objects.filter(
            id=self.kwargs['review_id'],
            title_id=self.kwargs['title_id']
        ).first()

    def get_queryset(self):
        return self.get_review().comments_by_review.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            review=review,
            title=review.title,
            author=self.request.user
        )


class TitleViewSet(viewsets.ModelViewSet):
    """Просмотр, редактирование и удаление произведений."""
    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Title.objects.annotate(
        rating_count=Avg('reviews_by_title__score')
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleWriteSerializer
