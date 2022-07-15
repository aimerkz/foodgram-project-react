from xml.dom import ValidationErr
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from recipes.models import (
    Tag, Ingredient, IngredientRecipes, Recipe)

from drf_extra_fields.fields import Base64ImageField


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор Тег"""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор Ингредиенты"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор Ингредиенты в рецепте"""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.CharField(source='ingredients.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredients.measurement_unit', read_only=True)

    class Meta:
        model = IngredientRecipes
        fields = ['id', 'name', 'measurement_unit', 'count']


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор Рецепт"""
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipesSerializer(
        many=True,
        source='ingredientrecipes_set',
        read_only=True
    )
    author=CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]

    def get_is_favorited(self, obj):
        """Метод проверки наличия рецепта в избранном"""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(recipefavorites__user=user, id=obj.id).exists()
    
    def get_is_in_shopping_cart(self, obj):
        """Метод проверки наличия рецепта в списке покупок"""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(shoppinglist__user=user, id=obj.id).exists()

    def validate(self, data):
        """Метод для валидации данных 
        перед созданием рецепта
        """
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'В рецепте отсутсвуют ингредиенты'})
        ingredients_result = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredient_item['id']
            )
            if ingredient in ingredients_result:
                raise serializers.ValidationError('Ингредиент уже добавлен в рецепт')
            ingredients_result.append(ingredient)
            if int(ingredient_item['count']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Ну указано количество ингредиента')
                })
        data['ingredients'] = ingredients_result
        return data

    def create(self, validated_data):
        """Метод для создания рецепта"""
        image = validated_data.pop('image')
        ingredients = validated_data['ingredients']
        recipes = Recipe.objects.create(
            image=image,
            **validated_data
        )
        tags = self.initial_data.get('tags')
        recipes.tags.set(tags)
        for ingredient in ingredients:
            IngredientRecipes.objects.create(
                recipes=recipes,
                ingredient=ingredient.get('id'),
                count=ingredient.get('count')
            )
        return recipes
