from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comments
from users.constants import (
    CONFIRMATION_CODE_LENGTH,
    EMAIL_MAX_LENGTH,
    MAX_LENGTH_FOR_FIELDS
)
from users.models import YaMDBUser
from users.validators import username_validate


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
    rating = serializers.IntegerField(default=0)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate(self, validated_data):
        genres = validated_data.get('genre')
        if self.context['request'].method == 'POST' and (
            genres is None or len(genres) == 0
        ):
            raise serializers.ValidationError(
                'Отсутствует обязательное поле или оно не корректно.'
            )
        return super().validate(validated_data)

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            title.genre.add(Genre.objects.get(name=genre))
        return title

    def to_representation(self, instance):
        return TitleSerializer(self).to_representation(instance)


class ReviewSerlizer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, validated_data):
        author = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']
        if (self.context['request'].method == 'POST'
                and Review.objects.filter(
                    title=title_id, author=author
        ).exists()):
            raise serializers.ValidationError(
                'Можно написать только один отзыв на произведение!'
            )
        return super().validate(validated_data)


class CommentSerlizer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        read_only_fields = ('review',)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_FOR_FIELDS,
        validators=[username_validate],
        required=True
    )
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH,
                                   required=True)


class UserRecieveTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,
                                     validators=[username_validate],
                                     max_length=MAX_LENGTH_FOR_FIELDS)
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YaMDBUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
