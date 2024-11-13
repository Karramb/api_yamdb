from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, TitleCreateSerializer
)
from api.models import Category, Genre, Title
from api.permissions import IsAdminOrReadOnly


class CategoryViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    # только добавление, чтение и удаление, остальное не по ТЗ
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # т к по ТЗ д быть удаление по ...categories/{slug}/
    lookup_field = 'slug'
    # чтение у всех, а добавление и удаление admin
    # permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # т к по ТЗ д быть удаление по ...genres/{slug}/
    lookup_field = 'slug'
    # чтение у всех, а добавление и удаление admin
    # permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # надо убрать put, но моему ревьюеру этот метод не нравился
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    # retrieve получения определённого объекта
    def get_serializer_class(self):
        # получения списка объектов или одного чтоб выводило категорию - словарь
        if self.action == 'list' or self.action == 'retrieve':
            return TitleSerializer
        if self.action == 'create':      # create создание объекта = post
            return TitleCreateSerializer
        return TitleSerializer