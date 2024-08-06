from typing import ClassVar

from django_filters import rest_framework as filters

from .models import MLModelsIndex


class MLModelsIndexFilter(filters.FilterSet):
    class Meta:
        model = MLModelsIndex
        fields: ClassVar[dict[str, list[str]]] = {
            "model_id": ["exact", "in"],
            "target_me": ["exact", "regex"],
            "active": ["exact"],
        }
