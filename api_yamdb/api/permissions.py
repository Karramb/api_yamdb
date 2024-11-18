from rest_framework import permissions

from users.models import UserRoles

# from users.models import CustomUser
# from users.models import ROLE


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (request.user.is_authenticated
                and (
                    request.user.role == UserRoles.admin.name
                    or request.user.is_superuser
                )
                )


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
