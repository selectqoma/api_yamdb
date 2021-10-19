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
        return (
            request.user.is_authenticated
            and request.user.role == 'moderator'
        )


class IsAdmin(permissions.BasePermission):
    """Проверяет, является ли пользователь админом."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверяет, является ли пользователь админом."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class AuthorOrReadOnlyPermission(permissions.BasePermission):
    """Проверяет, является ли пользователь автором объекта,
    модератором или админом."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in
            permissions.SAFE_METHODS or obj.author
            == request.user or request.user.role in ['admin', 'moderator']
        )
