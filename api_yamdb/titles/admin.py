from django.contrib import admin

from .models import Review, Title, Genre, Category, Comments

admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Comments)
