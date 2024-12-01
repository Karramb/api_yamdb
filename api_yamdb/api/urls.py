from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       ReviewViewSet, CommentViewSet,
                       UserSignUp, UserReceiveTokenV, UserViewSet)


router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register('users', UserViewSet, basename='users')


urls_for_auth = [
    path(
        'signup/',
        UserSignUp.as_view(),
        name='signup'
    ),
    path(
        'token/',
        UserReceiveTokenV.as_view(),
        name='token'
    )
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(urls_for_auth))
]
