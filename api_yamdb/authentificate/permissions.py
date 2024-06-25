from django.contrib.auth import get_user_model
from rest_framework import permissions


User = get_user_model()


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role.lower() == User.ROLE_ADMIN
                    or request.user.is_superuser)
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role.lower() == User.ROLE_ADMIN
                    or request.user.is_superuser)
        return False
