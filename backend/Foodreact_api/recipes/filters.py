from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag


class CustomSearchFilter(SearchFilter):
    """Кастомный сертч фильтр."""

    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    """Фильтрсет для Рецептов."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='favorite_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='shopping_cart_filter'
    )

    def favorite_filter(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value is True:
            return queryset.filter(recipe_to_favorite__author=user)
        return queryset

    def shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value is True:
            return queryset.filter(recipe_to_cart__author=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']
