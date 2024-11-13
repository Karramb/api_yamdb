from rest_framework import serializers

import datetime as dt

from api.models import Category, Genre, Title, TitleGenre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # временно оставим id для удобства
        # fields = '__all__'
        # вот так по ТЗ:
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        # временно оставим id для удобства
        # fields = '__all__'
        # вот так по ТЗ:
        fields = ('name', 'slug')


# так получаю корректный ответ на get запрос (как надо отображает категории):
class TitleSerializer(serializers.ModelSerializer):
    # Чтоб выводило как словарь:
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего."
            )
        return value


# ПО тз post запрос:
# # {
# "name": "string",
# "year": 0,
# "description": "string",
# "genre": [
# "string"
# ],
# "category": "string"    Строка!
# }:
# и вот так SlugRelatedFiel категорию сохранит
class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    # genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего."
            )
        return value
    
    def create(self, validated_data):
        # удаляем список slug жанров из входных данных пока, чтоб не мешал
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        return title
# А результат:
# {
# "id": 0,
# "name": "string",
# "year": 0,
# "rating": 0,
# "description": "string",
# "genre": [
# {
# "name": "string",
# "slug": "^-$"
# }
# ],
# "category": {        
# "name": "string",     Словарь! а это надо как 31 строке указать.
# "slug": "^-$"
# }
# }