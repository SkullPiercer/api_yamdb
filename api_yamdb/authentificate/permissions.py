from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role.lower() == 'admin'
                    or request.user.is_superuser)
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role.lower() == 'admin'
                    or request.user.is_superuser)
        return False
