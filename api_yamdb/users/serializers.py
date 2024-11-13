from rest_framework import serializers

from .models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Имя me запрещено')
        if (CustomUser.objects.filter(email=data['email'])
                or CustomUser.objects.filter(username=data['username'])):
            if not CustomUser.objects.filter(
                email=data['email'],
                username=data['username']
            ):
                raise serializers.ValidationError(
                    'Пользователь с такой почтой уже есть'
                )
        return data


class UserRecieveTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        if username in 'me':
            raise serializers.ValidationError(
                'Имя me запрещено'
            )
        return username
