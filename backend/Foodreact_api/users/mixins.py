from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CreateRetrieveListView(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.ListModelMixin, mixins.UpdateModelMixin,
    GenericViewSet
):
    pass
