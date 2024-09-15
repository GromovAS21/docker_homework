from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsUserProfile(permissions.BasePermission):
    """
    Проверяет, является ли профиль текущего пользовател
    """

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id
