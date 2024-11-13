from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # добавить провеку role = admin, а сейчас только на Суперпользователя Django
        # Даже если изменить пользовательскую роль суперпользователя — это не лишит его прав администратора. 
        # реализовать Ошибки: 401, 403
        return bool(request.user and request.user.is_staff)