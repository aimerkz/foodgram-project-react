from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from api.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    RecipeFavoritesSerializer, FollowSerializer, ShoppingListSerializer)
from api.pagination import CustomPagination
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

from recipes.models import (IngredientRecipes, Tag, Ingredient, Recipe, RecipeFavorites,
                            Follow, CustomUser, ShoppingList)

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсэт Тег
    Получение списка тегов / 
    конкретного тега
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсэт Ингредиенты
    Получение списка ингредиентов / 
    конкретного ингредиента
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсэт Рецепт
    Получение списка рецептов / 
    конкретного рецепта / from urllib import response

    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Метод для скачивания списка покупок"""
        shopping_result = {}
        ingredients = IngredientRecipes.objects.filter(
            recipes__shoppinglist__user=request.user
        ).values_list(
            'ingredients__name',
            'ingredients__measurement_unit',
            'amount'
        )

        for ingredient in ingredients:
            name = ingredient[0]
            if name not in shopping_result:
                shopping_result[name] = {
                    'measurement_unit': ingredient[1],
                    'amount': ingredient[2]
                }
            else:
                shopping_result[name]['amount'] += ingredient[2]

        shopping_itog = (f"{name} - {value['amount']} "
                        f"{value['measurement_unit']}\n"
                        for name, value in shopping_result.items()
        )
        response = HttpResponse(shopping_itog, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shoppinglist.txt"'
        return response


class RecipeFavoritesViewSet(viewsets.ModelViewSet):
    """Вьюсэт Списки избранных рецептов
    Добавление /
    удаление из списка
    """
    serializer_class = RecipeFavoritesSerializer
    queryset = RecipeFavorites.objects.all()
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
