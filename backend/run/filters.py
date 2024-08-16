from typing import ClassVar

from django_filters import rest_framework as filters
from utils import filters_mixins

from .models import Run


class RunFilter(filters_mixins.DatasetFilterMethods, filters.FilterSet):
    class Meta:
        model = Run
        fields: ClassVar[dict[str, list[str]]] = {
            "dataset_id": ["exact", "in"],
            "run_number": ["exact", "lte", "gte"],
        }
