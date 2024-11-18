from rest_framework import permissions

# from users.models import CustomUser
# from users.models import ROLE


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # на Суперпользователя Django
        # Даже если изменить пользовательскую роль суперпользователя — это не лишит его прав администратора.
        # реализовать Ошибки: 401, 403
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return True
        #  (request.method in permissions.SAFE_METHODS
        #         or custom_user.role == 'Admin')
        #         с подтягиванием константы думаю лучше:
        #         or custom_user.role == ROLE[3])

# Permissins для проверки
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            role = request.user.role
        else:
            role = 'anonim'
        return request.method in permissions.SAFE_METHODS or request.user == obj.author or role in ['moderator', 'admin']
