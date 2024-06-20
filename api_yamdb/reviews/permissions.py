from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (
                request.user == obj.author
                or request.user.role.lower() in ('admin', 'moderator')
            )
        return True


class IsAdmin(permissions.BasePermission):
    """Базовый доступ администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(IsAdmin):
    """Доступ на изменение/удаление только для администратора."""

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            or request.method in permissions.SAFE_METHODS
        )
