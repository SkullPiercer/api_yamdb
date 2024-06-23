from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.filters import TitleFilter
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.permissions import IsAuthorOrAdminOrReadOnly, IsAdminOrReadOnly
from reviews.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleWriteSerializer
)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Просмотр, редактирование и удаление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Просмотр, редактирование и удаление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewset(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    model = Review
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly, IsAuthenticatedOrReadOnly)
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = Title.objects.get(id=title_id)
        user = self.request.user
        serializer.save(title=title, author=user)


class CommentViewset(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    model = Comment
    queryset = Comment.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly, IsAuthenticatedOrReadOnly)
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
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleWriteSerializer
