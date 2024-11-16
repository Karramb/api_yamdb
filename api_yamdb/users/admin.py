from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'bio', 'role']
    list_display_links = ['email', 'username',]
    list_editable = ['bio', 'role']
