from rest_framework import permissions

from .models import User


class AuthorPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author
                or request.user.is_staff
                or request.user.role == User.ADMIN
                or request.user.role == User.MODERATOR)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return bool(
                request.user.is_staff or request.user.role == User.ADMIN)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool((request.user.role == User.ADMIN)
                        or (request.user.is_staff
                            and request.user.is_superuser))
