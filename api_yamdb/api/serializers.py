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


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=0)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleNotReadSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True,
        allow_empty=False,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def to_representation(self, instance):
        return TitleReadSerializer(self).to_representation(instance)


class ReviewSerlizer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, validated_data):
        author = self.context['request'].user
        title = self.context['view'].kwargs['title_id']
        if (Review.objects.filter(title=title, author=author).exists()
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                'Один пользвователь - один отзыв'
            )
        return super().validate(validated_data)


class CommentSerlizer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
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
