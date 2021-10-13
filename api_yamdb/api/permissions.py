from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Неавторизованные пользователи доступно только чтение."""

    def has_permission(self, request, view):
        return (
                request.method in
                permissions.SAFE_METHODS or request.user.is_authenticated
        )


class IsAuthor(permissions.BasePermission):
    """Проверяет, является ли пользователь автором."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsModerator(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'moderator'


class IsAdmin(permissions.BasePermission):
    """Проверяет, является ли пользователь админом."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'admin'
