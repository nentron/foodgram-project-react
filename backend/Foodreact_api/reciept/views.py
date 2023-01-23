from rest_framework import (
    filters, viewsets, pagination,
    response, status
)
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.conf import settings

from .mixins import GetListViewset
from .models import (
    Ingredient, Tag, Reciept, FavoriteReciepes,
    ShoppingCart, IngredientAmount
)
from .serializers import (
    IngredientSerializer, TagSerializer,
    RecieptSerializer, RecipesSerializer
)
from .permissions import AuthorOrSaveMethods
from .filters import RecieptFilter


User = get_user_model()


class IngredientViewset(GetListViewset):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class TagViewset(GetListViewset):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecieptViewset(viewsets.ModelViewSet):
    queryset = Reciept.objects.all()
    serializer_class = RecieptSerializer
    pagination_class = (pagination.LimitOffsetPagination)
    permission_classes = [AuthorOrSaveMethods]
    filterset_class = RecieptFilter

    @action(methods=['GET'], detail=False)
    def favorites(self, request):
        queryset = Reciept.objects.filter(
            reciept_to_favorite__author=request.user
        )
        results = self.paginate_queryset(queryset)
        serializer = RecipesSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST', 'DELETE'],
            detail=True)
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            obj = FavoriteReciepes.objects.create(
                author=request.user, reciept_id=pk
            )
            serializer = RecipesSerializer(instance=obj.reciept)
            return response.Response(serializer.data)
        request.user.author_favorite.filter(reciept_id=pk).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def download_shopping_cart(self, request):
        ingredients = IngredientAmount.objects.filter(
            reciept__reciept_to_cart__author=request.user
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
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            obj = ShoppingCart.objects.create(
                author=request.user, reciept_id=pk
            )
            serializer = RecipesSerializer(obj.reciept)
            return response.Response(serializer.data)
        request.user.usercart.filter(reciept_id=pk).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
