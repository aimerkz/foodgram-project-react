from django_filters.rest_framework import FilterSet, filters

from users.models import CustomUser
from recipes.models import Recipe


class RecipesFilter(FilterSet):
    """Кастомный фильтр для рецептов по
    избранному, автору, списку покупок и
    тегам"""
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())

    class Meta:
        model = Recipe
        fields = ['author']
