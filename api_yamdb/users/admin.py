from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import YaMDBUser


@admin.register(YaMDBUser)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'role')
    list_display_links = ('email', 'username')
    list_editable = ('role',)
