from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from recipes.models import (
    Tag, Ingredient, IngredientRecipes, Recipe, RecipeFavorites,
    Follow)

from drf_extra_fields.fields import Base64ImageField


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор Теги"""
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
        fields = ['id', 'name', 'measurement_unit', 'amount']


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
            amount=ingredient_item['amount']
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Не указано количество ингредиента')
                })
            ingredients_result.append({'ingredients': ingredient, 'amount': amount})
        data['ingredients'] = ingredients_result
        return data

    def create_ingredients(self, ingredients, recipes):
        """Метод для добавления ингредиентов"""
        for ingredient in ingredients:
            IngredientRecipes.objects.create(
                recipes=recipes,
                ingredients=ingredient['ingredients'],
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        """Метод для создания рецепта"""
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipes = Recipe.objects.create(
            image=image,
            **validated_data
        )
        tags = self.initial_data.get('tags')
        recipes.tags.set(tags)
        self.create_ingredients(ingredients_data, recipes)
        return recipes

    def update(self, instance, validated_data):
        """Метод для обновления рецепта"""
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientRecipes.objects.filter(recipes=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance


class RecipeFavoritesSerializer(serializers.ModelSerializer):
    """Сериализатор Списки избранных рецептов"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = Base64ImageField(max_length=None, use_url=False,)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = RecipeFavorites
        fields = ['id', 'name', 'image', 'cooking_time']
        validators = (
            UniqueTogetherValidator(
                queryset=RecipeFavorites.objects.all(),
                fields=('user', 'recipes')
            )
        )


class FollowRecipeSerializer(serializers.ModelSerializer):
    """Урезанный сериализатор Рецепты для сериализатора Подписки ниже"""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ['id', 'name', 'image', 'cooking_time']


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор Подписки"""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username =  serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes',
                  'recipes_count'
        ]

    def get_is_subscribed(self, obj):
        """Метод для проверки подписки
        текущего юзера на автора
        """
        return Follow.objects.filter(
            user=obj.user,
            author=obj.author
        ).exists()
        
    def get_recipes(self, obj):
        """Метод для получения
        рецептов автора
        """
        queryset = Recipe.objects.filter(
            author=obj.author
        )
        return FollowRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """Метод для получения общего
        количества рецептов автора
        """
        return Recipe.objects.filter(author=obj.author).count()
