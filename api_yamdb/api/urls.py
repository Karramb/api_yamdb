from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       ReviewViewSet, CommentViewSet)
from users.views import UserCreateViewSet, UserReceiveTokenViewSet, UserViewSet


signup = UserCreateViewSet.as_view({'post': 'create'})
token = UserReceiveTokenViewSet.as_view({'post': 'create'})

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


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
]
