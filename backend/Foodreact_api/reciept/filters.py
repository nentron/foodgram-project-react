from django_filters import rest_framework as filters

from .models import Reciept, Tag


class RecieptFilter(filters.FilterSet):
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
            return queryset.filter(reciept_to_favorite__author=user)
        return queryset

    def shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value is True:
            return queryset.filter(reciept_to_cart__author=user)
        return queryset

    class Meta:
        model = Reciept
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']
