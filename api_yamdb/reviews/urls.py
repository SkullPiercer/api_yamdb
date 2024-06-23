from django.urls import include, path
from rest_framework import routers

from reviews.views import (
    CategoryViewSet, CommentViewset, GenreViewSet, ReviewViewset, TitleViewSet
)

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewset,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewset,
    basename='comments'
)

urlpatterns = [
    path('', include(v1_router.urls))
]
