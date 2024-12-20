from typing import ClassVar

from django_filters import rest_framework as filters
from utils import filters_mixins

from .models import MLBadLumisection


class MLBadLumisectionFilter(filters_mixins.DatasetFilterMethods, filters_mixins.MEsMethods, filters.FilterSet):
    class Meta:
        model = MLBadLumisection
        fields: ClassVar[dict[str, list[str]]] = {
            "model_id": ["exact", "in"],
            "dataset_id": ["exact", "in"],
            "me_id": ["exact"],
            "run_number": ["exact", "in"],
            "ls_number": ["exact"],
        }
