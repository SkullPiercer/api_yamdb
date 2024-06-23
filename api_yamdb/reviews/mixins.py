from rest_framework import mixins, viewsets

from .permissions import IsAdminOrReadOnly


class GenreCategoryBaseMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для жанров и категорий."""

    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("name",)
    lookup_field = "slug"
