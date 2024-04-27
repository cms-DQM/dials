from typing import ClassVar

from django_filters import rest_framework as filters
from utils import filters_mixins

from .models import TH2


class TH2Filter(
    filters_mixins.DatasetFilterMethods, filters_mixins.MEsMethods, filters_mixins.FileIndexMethods, filters.FilterSet
):
    class Meta:
        model = TH2
        fields: ClassVar[dict[str, list[str]]] = {
            "dataset_id": ["exact"],
            "file_id": ["exact"],
            "run_number": ["exact", "lte", "gte"],
            "ls_number": ["exact", "lte", "gte"],
            "me_id": ["exact"],
            "ls_id": ["exact"],
            "entries": ["gte"],
        }
