from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.permissions import IsAuthorOrReadOnly
from reviews.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Comment, Review, Title


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewset(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    model = Review
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
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
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        title_id = self.kwargs['title_id']
        title = Title.objects.get(id=title_id)
        review = Review.objects.get(id=review_id)
        user = self.request.user
        serializer.save(review=review, title=title, author=user)


class TitleViewSet(viewsets.ModelViewSet):
    pass
