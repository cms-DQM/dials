from typing import ClassVar

from django_filters import rest_framework as filters
from utils import filters_mixins

from .models import TH1


class TH1Filter(
    filters_mixins.DatasetFilterMethods, filters_mixins.MEsMethods, filters_mixins.FileIndexMethods, filters.FilterSet
):
    class Meta:
        model = TH1
        fields: ClassVar[dict[str, list[str]]] = {
            "dataset_id": ["exact"],
            "file_id": ["exact"],
            "run_number": ["exact", "lte", "gte"],
            "ls_number": ["exact", "lte", "gte"],
            "me_id": ["exact"],
            "entries": ["gte"],
        }
