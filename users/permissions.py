from rest_framework import permissions


class Moderator(permissions.BasePermission):
    """
    Разрешение на уровне объекта, позволяющее добавлять и изменять объекты только для модераторов.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    """
    Проверка пользователя на владение объектом
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
