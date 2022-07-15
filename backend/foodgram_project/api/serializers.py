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


class RecipeSerializer(serializers.Serializer):
    """Сериализатор Рецепт"""
    id = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipesSerializer(
        read_only=True,
        many=True,
        source='ingredientrecipes_set'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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
            'cooking_time'
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
