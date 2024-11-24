from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets

from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer,
    TitleCreateSerializer, ReviewSerlizer, CommentSerlizer
)
from reviews.models import Category, Genre, Title, Review


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
    serializer_class = TitleSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleSerializer
        else:
            return TitleCreateSerializer

    def get_queryset(self):
        return Title.objects.annotate(
            rating=models.Avg('reviews__score')).order_by('name')


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
