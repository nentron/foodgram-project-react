from rest_framework import filters

from .mixins import GetListViewset
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewset(GetListViewset):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']
