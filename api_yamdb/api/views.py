from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError, models
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters, generics, mixins, permissions, serializers, status, viewsets
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, OnlyAdmin
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleReadSerializer,
    TitleWriteSerializer, ReviewSerlizer, CommentSerlizer,
    SignupSerializer, UserRecieveTokenSerializer, UserSerializer
)
from api_yamdb.settings import DEFAULT_FROM_EMAIL, RESERVED_NAME
from reviews.models import Category, Genre, Title, Review
from users.models import YaMDBUser


class OptionsViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(OptionsViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(OptionsViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=models.Avg('reviews__score')
    ).order_by('-rating', *Title._meta.ordering)
    serializer_class = TitleReadSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerlizer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsOwnerOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerlizer
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs['review_id'], title=self.kwargs['title_id']
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )

    def get_queryset(self):
        return self.get_review().comments.all()


class UserSignUp(generics.CreateAPIView):
    queryset = YaMDBUser.objects.all()
    serializer_class = SignupSerializer()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = YaMDBUser.objects.get_or_create(
                **serializer.validated_data
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Пользователь c {} уже существует.'.format(
                    "Никнейм" if YaMDBUser.objects.filter(
                        email=request.data.get('username')
                    ).exists() else "email"
                )
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email, ],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReceiveTokenV(APIView):
    queryset = YaMDBUser.objects.all()
    serializer_class = UserRecieveTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRecieveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            YaMDBUser,
            username=request.data.get('username')
        )
        confirmation_code = request.data.get('confirmation_code')
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                'Ошибка в коде подтверждения.')
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = YaMDBUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (OnlyAdmin,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False,
            methods=['get'],
            url_path=RESERVED_NAME,
            permission_classes=(IsAuthenticated,))
    def self_data(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @self_data.mapping.patch
    def patch_self_data(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
