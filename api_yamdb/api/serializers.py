from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from reviews.models import Category, Genre, Title, Review, Comments
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from users.constants import EMAIL_MAX_LENGTH, MAX_LENGTH_FOR_FIELDS
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


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_FOR_FIELDS,
        validators=[username_validate]
    )
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)

    class Meta:
        model = YaMDBUser
        fields = ('username', 'email')

    def validate(self, data):
        if YaMDBUser.objects.filter(
            email=data.get('email')) or YaMDBUser.objects.filter(
                username=data.get('username')):
            if YaMDBUser.objects.filter(email=data.get('email'),
                                         username=data.get('username')):
                pass
            else:
                raise serializers.ValidationError(
                    'Пользователь с такими данными уже есть в системе')
        return data

    def create(self, validated_data):
        serializer = UserCreateSerializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        user, _ = YaMDBUser.objects.get_or_create(
            **serializer.validated_data
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email, ],
            fail_silently=True,
        )
        return validated_data


class UserRecieveTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(YaMDBUser, username=data.get('username'))
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                'Ошибка в коде подтверждения.')
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'token': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YaMDBUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
