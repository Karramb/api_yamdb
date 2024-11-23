from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comments


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
    # Неверный тип сериализатора ПАЧКА
    genre = serializers.ListField(write_only=True)

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
            title.genre.add(Genre.objects.get(slug=genre))
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
