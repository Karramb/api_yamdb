from rest_framework import permissions

from .models import UserRoles


class OnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (
                    request.user.role == UserRoles.admin.name
                    or request.user.is_superuser
                )
                )
