from rest_framework import serializers

import datetime as dt

from titles.models import Category, Genre, Title, TitleGenre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
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
        for genre in genres:
            if not Genre.objects.filter(slug=genre).exists():
                raise serializers.ValidationError(
                    "Отсутствует обязательное поле или оно не корректно."
                )
        title = Title.objects.create(**validated_data)
        for genre in genres:
            TitleGenre.objects.create(title=title, genre=Genre.objects.get(slug=genre))
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)

        genres = validated_data.pop('genre')
        print(genres)
        lst = []
        for genre in genres:
            if not Genre.objects.filter(slug=genre).exists():
                raise serializers.ValidationError(
                    "Отсутствует обязательное поле или оно не корректно."
                )
            current_genre = Genre.objects.get(slug=genre)
            lst.append(current_genre)
            instance.genre.set(lst)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # добавляю категории
        # representation['category'] = 'test'
        # добавляю жанр
        # representation['genre'] = 'test'
        return representation
