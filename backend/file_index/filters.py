from typing import ClassVar

from django_filters import rest_framework as filters
from utils import filters_mixins

from .models import FileIndex


class FileIndexFilter(filters_mixins.DatasetFilterMethods, filters.FilterSet):
    min_size = filters.NumberFilter(field_name="file_size", lookup_expr="gte")

    class Meta:
        model = FileIndex
        fields: ClassVar[dict[str, list[str]]] = {
            "dataset_id": ["exact"],
            "logical_file_name": ["exact", "regex"],
            "status": ["exact"],
        }
