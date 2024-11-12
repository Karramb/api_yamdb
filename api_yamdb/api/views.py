# from django.shortcuts import render
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
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


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination