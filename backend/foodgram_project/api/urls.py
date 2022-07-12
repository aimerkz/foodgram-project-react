from rest_framework import routers

from django.urls import include, path

from api.views import TagViewSet
from users.views import CustomUserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
