from django_filters.rest_framework import FilterSet, filters

from users.models import CustomUser
from recipes.models import Recipe

obj = dict({'recipefavorites': '', 'shoppinglist': ''})


class RecipesFilter(FilterSet):
    """Кастомный фильтр для рецептов по
    избранному, автору, списку покупок и
    тегам"""
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def _custom_filter(self, recipefavorites, shoppinglist, value, queryset):
        for key in obj.keys():
            if key == 'recipefavorites':
                if value and not self.request.user.is_anonymous:
                    return queryset.filter(
                        **{f'{key}__user': self.request.user})
            elif key == 'shoppinglist':
                if value and not self.request.user.is_anonymous:
                    return queryset.filter(
                        **{f'{key}__user': self.request.user})
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags']

    # def filter_is_favorited(self, queryset, name, value):
    #    if value and not self.request.user.is_anonymous:
    #        return queryset.filter(recipefavorites__user=self.request.user)
    #    return queryset

    # def filter_is_in_shopping_cart(self, queryset, name, value):
    #    if value and not self.request.user.is_anonymous:
    #        return queryset.filter(shoppinglist__user=self.request.user)
    #    return queryset
