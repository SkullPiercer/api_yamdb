from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from reviews.filters import TitleFilter
from reviews.mixins import GenreCategoryBaseMixin, ReviewCommentMixin
from reviews.models import Category, Comment, Genre, Review, Title
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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = Title.objects.get(id=title_id)
        user = self.request.user
        serializer.save(title=title, author=user)


class CommentViewset(ReviewCommentMixin):
    """Просмотр, редактирование и удаление комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        title_id = self.kwargs['title_id']
        title = Title.objects.get(id=title_id)
        review = Review.objects.get(id=review_id)
        user = self.request.user
        serializer.save(review=review, title=title, author=user)


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
