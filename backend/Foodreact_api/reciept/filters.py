from django_filters import rest_framework as filters

from .models import Reciept, Tag


class RecieptFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Reciept
        fields = ['author', 'tags']
