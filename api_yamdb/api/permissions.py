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

    # def has_object_permission(self, request, view, obj):
    #     return (request.method in permissions.SAFE_METHODS
    #             or custom_user.role == 'Admin')
    #             с подтягиванием константы думаю лучше:
    #             or custom_user.role == ROLE[3])


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
