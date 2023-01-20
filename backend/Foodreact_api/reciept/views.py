from rest_framework import (
    filters, viewsets, pagination,
    response, status
)
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from .mixins import GetListViewset
from .models import Ingredient, Tag, Reciept, FavoriteReciepes
from .serializers import (
    IngredientSerializer, TagSerializer,
    RecieptSerializer, RecipesSerializer,
    FavoriteSerializer
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
        queryset = request.user.author_favorite.all(
            ).select_related('reciept')
        results = self.paginate_queryset(queryset)
        serializer = FavoriteSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST', 'DELETE'],
            detail=True)
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            obj = FavoriteReciepes.objects.create(
                author=request.user, reciept_id=pk
            )
            serializer = FavoriteSerializer(instance=obj)
            return response.Response(serializer.data)
        request.user.author_favorite.filter(reciept_id=pk).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
