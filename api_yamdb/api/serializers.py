from rest_framework import serializers

import datetime as dt

from reviews.models import Category, Genre, Title, TitleGenre, Review, Comments


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.ListField(write_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        TitleGenre.objects.bulk_create(
            TitleGenre(
                title=title, genre=Genre.objects.get(slug=genre)
            ) for genre in genres
        )
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.category = validated_data.get('category', instance.category)
        instance.genre.set(
            Genre.objects.filter(slug__in=validated_data.pop('genre'))
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        answer = super().to_representation(instance)
        if (self.context['request'].method == 'POST'
                or self.context['request'].method == 'PATCH'):
            answer['category'] = CategorySerializer(
                instance.category, many=False
            ).data
            answer['genre'] = CategorySerializer(
                instance.genre, many=True
            ).data
        return answer


class ReviewSerlizer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть в диапазоне от 1 до 10'
            )
        return value


class CommentSerlizer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('review',)
