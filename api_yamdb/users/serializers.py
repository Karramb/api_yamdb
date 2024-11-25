from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.constants import EMAIL_MAX_LENGTH, MAX_LENGTH_FOR_FIELDS
from users.models import CustomUser
from users.validators import username_validate


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_FOR_FIELDS,
        validators=[username_validate]
    )
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate(self, data):
        if CustomUser.objects.filter(
            email=data.get('email')) or CustomUser.objects.filter(
                username=data.get('username')):
            if CustomUser.objects.filter(email=data.get('email'),
                                         username=data.get('username')):
                pass
            else:
                raise serializers.ValidationError(
                    'Пользователь с такими данными уже есть в системе')
        return data

    def create(self, validated_data):
        serializer = UserCreateSerializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        user, _ = CustomUser.objects.get_or_create(
            **serializer.validated_data
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Код подтверждения: {confirmation_code}',
            from_email='birthday_form@acme.not',
            recipient_list=[user.email, ],
            fail_silently=True,
        )
        return validated_data


class UserRecieveTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(CustomUser, username=data.get('username'))
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
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
