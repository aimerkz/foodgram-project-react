from rest_framework import routers

from django.urls import include, path, re_path

from api.views import (
    TagViewSet, IngredientsViewSet, RecipeViewSet,
    RecipeFavoritesViewSet)
from users.views import CustomUserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('users', CustomUserViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('recipes/<id>/favorite/',
        RecipeFavoritesViewSet.as_view({'post': 'create',
                                        'delete': 'delete'}), name='favorite'),
]
