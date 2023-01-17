from rest_framework import filters, viewsets, pagination

from .mixins import GetListViewset
from .models import Ingredient, Tag, Reciept
from .serializers import (
    IngredientSerializer, TagSerializer,
    RecieptSerializer
)
from .permissions import AuthorOrSaveMethods
from .filters import RecieptFilter


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
