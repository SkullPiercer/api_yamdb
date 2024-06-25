from django.contrib.auth import get_user_model
from rest_framework import permissions


User = get_user_model()


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.role == User.ROLE_ADMIN
            )
        )


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (
                request.user == obj.author
                or request.user.role.lower() in (User.ROLE_ADMIN, User.ROLE_MODERATOR)
            )
        return True
