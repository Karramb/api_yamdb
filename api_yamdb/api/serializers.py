from rest_framework import serializers

import datetime as dt

from api.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # временно оставим id для удобства
        fields = '__all__'
        # вот так в будущем:
        # fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        # временно оставим id для удобства
        fields = '__all__'
        # вот так в будущем:
        # fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'
    
    def validate_year(self, value):
        if value > dt.datetime.now().year:
            return serializers.ValidationError(
                "Год выпуска не может быть больше текущего."
            )
        return value
