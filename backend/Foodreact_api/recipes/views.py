from rest_framework import (
    viewsets, pagination,
    response, status, permissions
)
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .mixins import GetListViewset
from .models import (
    Ingredient, Tag, Recipe, FavoriteRecipes,
    ShoppingCart, IngredientAmount
)
from .serializers import (
    IngredientSerializer, TagSerializer,
    RecipeSerializer, RecipesSerializer,
    FavoriteSerializer, ShoppingCartSerializer
)
from .permissions import AuthorOrSaveMethods
from .filters import RecipeFilter, CustomSearchFilter
from .services import create_ingredients_list


User = get_user_model()


class IngredientViewset(GetListViewset):
    """Вьюсет для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['^name']
    pagination_class = None


class TagViewset(GetListViewset):
    """Вьюсет для тагов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewset(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = (pagination.LimitOffsetPagination)
    default_limit = 6
    permission_classes = [AuthorOrSaveMethods]
    filterset_class = RecipeFilter

    @staticmethod
    def __post_delete(request, model, created_model, serializer, pk):
        recipe = get_object_or_404(model, pk=pk)
        if request.method == 'POST':
            serializer = serializer(
                data={'author': request.user.pk,
                      'recipe': recipe.pk}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(serializer.data)
        got_obj = get_object_or_404(
            created_model,
            author=request.user,
            recipe=recipe
        )
        got_obj.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def favorites(self, request):
        queryset = Recipe.objects.filter(
            recipe_to_favorite__author=request.user
        )
        results = self.paginate_queryset(queryset)
        serializer = RecipesSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST', 'DELETE'],
            detail=True, permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        return self.__post_delete(
            request, Recipe, FavoriteRecipes,
            FavoriteSerializer, pk
        )

    @action(methods=['GET'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientAmount.objects.filter(
            recipe__recipe_to_cart__author=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount_sum=Sum('amount', distinct=True))
        response = HttpResponse(headers={
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename="ingredients.txt"'
        })
        ingredient_list = create_ingredients_list(ingredients)
        response.writelines(ingredient_list)
        return response

    @action(
        methods=['DELETE', 'POST'], detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return self.__post_delete(
            request, Recipe, ShoppingCart,
            ShoppingCartSerializer, pk
        )
