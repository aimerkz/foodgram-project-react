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
    list_display = ('name', 'author', 'count_favorited')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'

    def count_favorited(self, obj):
        """Метод выводит общее число добавлений рецепта в избранное"""
        return obj.recipefavorites_set.count()


class IngredientRecipesAdmin(admin.ModelAdmin):
    list_display = ('ingredients', 'recipes', 'amount')


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipes', 'tags')


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    search_fields = ('user', 'recipes')
    list_filter = ('user', 'recipes')


class RecipeFavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    search_fields = ('user', 'recipes')
    list_filter = ('user', 'recipes')


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
