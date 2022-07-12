from django.contrib import admin
from recipes.models import (
    Tag, Ingredient, Recipe, RecipeFavorites, IngredientRecipes, RecipeTag,
    ShoppingList, RecipeFavorites, Follow)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tag')
    empty_value_display = '-пусто-'

    def count_favorited(self, obj):
        """Метод выводит общее число добавлений рецепта в избранное"""
        return RecipeFavorites.objects.filter(recipe=obj).count()


class IngredientRecipesAdmin(admin.ModelAdmin):
    list_display = ('ingredients', 'recipes', 'count')


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tag')


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


class RecipeFavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipes, IngredientRecipesAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(RecipeFavorites, RecipeFavoritesAdmin)
admin.site.register(Follow, FollowAdmin)
