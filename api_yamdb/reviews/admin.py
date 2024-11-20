from django.contrib import admin

from .models import Review, Title, TitleGenre, Genre, Category, Comments
from .forms import TitleForm, ReviewForm

# Вместо пустого значения в админке будет отображена строка "Не задано".
admin.site.empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


class TitleGenreInline(admin.TabularInline):
    model = TitleGenre
    min_num = 1
    extra = 1


class TitleAdmin(admin.ModelAdmin):
    form = TitleForm
    list_display = ('name', 'year', 'description', 'category', 'get_genre')
    # какие поля можно редактировать прямо на странице списка объектов
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('category',)
    # поля, при клике на которые можно перейти на страницу просмотра и редактирования записи. 
    list_display_links = ('name',)
    inlines = (TitleGenreInline,)

    def get_genre(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    get_genre.short_description = 'Жанр(ы)'

admin.site.register(Title, TitleAdmin)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'score', 'pub_date', 'author')
    form = ReviewForm
    search_fields = ('title', 'text')
    list_filter = ('score', 'pub_date', 'author')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('text', 'review', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')


