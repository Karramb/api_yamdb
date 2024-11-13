from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from users.views import UserCreateViewSet, UserReceiveTokenViewSet, UserViewSet


signup = UserCreateViewSet.as_view({'post': 'create'})
token = UserReceiveTokenViewSet.as_view({'post': 'create'})

router = routers.DefaultRouter()
router.register('api/v1/users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', signup, name='signup'),
    path('api/v1/auth/token/', token, name='token'),
    path('', include(router.urls)),
]
