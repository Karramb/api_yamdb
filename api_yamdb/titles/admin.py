from django.contrib import admin

from .models import Reviews, Title, Genre, Category, Comments

admin.site.register(Reviews)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Comments)
