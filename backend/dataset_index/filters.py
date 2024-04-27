from typing import ClassVar

from django_filters import rest_framework as filters

from .models import DatasetIndex


class DatasetIndexFilter(filters.FilterSet):
    class Meta:
        model = DatasetIndex
        fields: ClassVar[dict[str, list[str]]] = {
            "dataset": ["exact", "regex"],
        }
