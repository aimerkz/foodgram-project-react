from api.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer)
from api.pagination import CustomPagination
from recipes.models import Tag, Ingredient, Recipe

from rest_framework import viewsets, status

from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(responses={status.HTTP_200_OK: TagSerializer()})
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсэт Тег
    Получение списка тегов / 
    конкретного тега
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPagination


@swagger_auto_schema(responses={status.HTTP_200_OK: IngredientSerializer()})
class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсэт Ингредиенты
    Получение списка ингредиентов / 
    конкретного ингредиента"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = CustomPagination


@swagger_auto_schema(responses={status.HTTP_200_OK: RecipeSerializer()})
class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсэт Рецепт
    Получение списка рецептов / 
    конкретного рецепта / 
    создание рецепта / 
    частичное изменение рецепта / 
    удаление рецепта
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
