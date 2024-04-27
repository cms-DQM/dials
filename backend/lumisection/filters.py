from typing import ClassVar

from django_filters import rest_framework as filters
from utils import filters_mixins

from .models import Lumisection


class LumisectionFilter(filters_mixins.DatasetFilterMethods, filters.FilterSet):
    class Meta:
        model = Lumisection
        fields: ClassVar[dict[str, list[str]]] = {
            "dataset_id": ["exact"],
            "run_number": ["exact", "lte", "gte"],
            "ls_number": ["exact", "lte", "gte"],
        }
