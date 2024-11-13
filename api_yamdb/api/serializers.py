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


# для get запроса
class TitleSerializer(serializers.ModelSerializer):
    # Чтоб выводило как словарь:
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'


# для post запроса
class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    genre = serializers.ListField(write_only=True)

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
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            id = Genre.objects.get(slug=genre)
            TitleGenre.objects.create(title=title, genre=id)
        return title
