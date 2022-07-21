from django.shortcuts import get_object_or_404
from api.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    RecipeFavoritesSerializer, FollowSerializer, ShoppingListSerializer)
from api.pagination import CustomPagination
from recipes.models import (Tag, Ingredient, Recipe, RecipeFavorites,
                            Follow, CustomUser, ShoppingList)

from rest_framework import viewsets, status
from rest_framework.response import Response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсэт Тег
    Получение списка тегов / 
    конкретного тега
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPagination


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсэт Ингредиенты
    Получение списка ингредиентов / 
    конкретного ингредиента
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = CustomPagination


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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeFavoritesViewSet(viewsets.ModelViewSet):
    """Вьюсэт Списки избранных рецептов
    Добавление /
    удаление из списка
    """
    serializer_class = RecipeFavoritesSerializer
    queryset = RecipeFavorites.objects.all()

    def create(self, request, *args, **kwargs):
        """Метод для добавления рецепта
        в список избранного
        """
        recipes_id = self.kwargs['id']
        recipes = get_object_or_404(Recipe, id=recipes_id)
        RecipeFavorites.objects.create(
            user=request.user,
            recipes=recipes
        )
        serializer = RecipeFavoritesSerializer()
        return Response(serializer.to_representation(instance=recipes),
                        status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        """Метод для удаления рецепта
        из списка избранного
        """
        recipes_id = self.kwargs['id']
        user_id = request.user.id
        object = get_object_or_404(
            RecipeFavorites, user__id=user_id,
            recipes__id=recipes_id
        )
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсэт Подписки
    Cоздание подписки / 
    удаление подписки
    """
    serializer_class = FollowSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        """Метод для создания подписки"""
        user_id = self.kwargs['id']
        user = get_object_or_404(CustomUser, id=user_id)
        subscribe = Follow.objects.create(
            user=request.user, author=user)
        serializer = FollowSerializer(subscribe,
                                      context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Метод для удаления подписки"""
        author_id = self.kwargs['id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Follow, user__id=user_id, author__id=author_id)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingViewSet(viewsets.ModelViewSet):
    """Вьюсэт Список покупок
    Добавление рецепта в список покупок /
    удаление рецепта из списка покупок /
    скачивание списка покупок
    """
    serializer_class = ShoppingListSerializer
    pagination_class = CustomPagination
    queryset = ShoppingList.objects.all()

    def create(self, request, *args, **kwargs):
        """Метод для добавление рецепта в 
        список покупок
        """
        recipe_id = self.kwargs['id']
        recipes = get_object_or_404(Recipe, id=recipe_id)
        ShoppingList.objects.create(
            user=request.user,
            recipes=recipes
        )
        serializer = ShoppingListSerializer()
        return Response(serializer.to_representation(instance=recipes),
                        status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Метод для удаление рецепта из
        списка покупок
        """
        recipe_id = self.kwargs['id']
        user_id = request.user.id
        object = get_object_or_404(
            ShoppingList, user__id=user_id, recipes__id=recipe_id
        )
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
