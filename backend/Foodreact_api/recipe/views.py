from rest_framework import (
    filters, viewsets, pagination,
    response, status, permissions
)
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.conf import settings
from django.shortcuts import get_object_or_404

from .mixins import GetListViewset
from .models import (
    Ingredient, Tag, Recipe, FavoriteRecipes,
    ShoppingCart, IngredientAmount
)
from .serializers import (
    IngredientSerializer, TagSerializer,
    RecipeSerializer, RecipesSerializer
)
from .permissions import AuthorOrSaveMethods
from .filters import RecipeFilter


User = get_user_model()


class IngredientViewset(GetListViewset):
    """Вьюсет для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class TagViewset(GetListViewset):
    """Вьюсет для тагов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewset(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = (pagination.LimitOffsetPagination)
    permission_classes = [AuthorOrSaveMethods]
    filterset_class = RecipeFilter

    @staticmethod
    def __post_delete(request, model, created_model, pk):
        recipe = get_object_or_404(model, pk=pk)
        if request.method == 'POST':
            obj, created = created_model.objects.get_or_create(
                author=request.user, recipe=recipe
            )
            if created is False:
                return response.Response(
                    {'datail': 'Can not add object twice'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = RecipesSerializer(instance=obj.recipe)
            return response.Response(serializer.data)
        try:
            got_obj = created_model.objects.get(
                author=request.user,
                recipe=recipe
            )
        except Exception:
            return response.Response(
                {'datail': 'object does not exist'},
                status=status.HTTP_400_BAD_REQUEST
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
            request, Recipe, FavoriteRecipes, pk
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
        f = open(
            f'{settings.MEDIA_ROOT}/{request.user}.txt',
            'w+', encoding='utf8'
        )
        for row in ingredients:
            f.write(
                '{0} ({1}) - {2}\n'.format(
                    row.get('ingredient__name'),
                    row.get('ingredient__measurement_unit'),
                    row.get('amount_sum')
                )
            )
        return FileResponse(f)

    @action(
        methods=['DELETE', 'POST'], detail=True,
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return self.__post_delete(
            request, Recipe, ShoppingCart, pk
        )
