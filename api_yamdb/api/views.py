from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.core.exceptions import BadRequest
from django.db import models

from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, TitleCreateSerializer, ReviewSerlizer, CommentSerlizer
)
from titles.models import Category, Genre, Title, Reviews
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class CategoryViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
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
    lookup_field = 'slug'
    # чтение у всех, а добавление и удаление admin
    # permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    # надо убрать put, но моему ревьюеру этот метод не нравился
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleSerializer
        if self.action == 'create' or self.action == 'partial_update':
            return TitleCreateSerializer
        return TitleSerializer

    def get_queryset(self):
        return Title.objects.annotate(rating=models.Avg('reviews__score'))


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerlizer
    # permission_classes = (IsOwnerOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def perform_create(self, serializer):
        try:
            serializer.save(
                # author=self.request.user,
                author=9,
                title=self.get_title(),
            )
        except Exception:
            raise BadRequest("Один пользвователь - один отзыв")

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerlizer
    # permission_classes = (IsOwnerOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Reviews, pk=self.kwargs['review_id'])

    def perform_create(self, serializer):
        serializer.save(
            # author=self.request.user,
            author=1,
            review=self.get_review()
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()
