from typing import ClassVar

from django_filters import rest_framework as filters

from .models import MEs


class MEsFilter(filters.FilterSet):
    class Meta:
        model = MEs
        fields: ClassVar[dict[str, list[str]]] = {"me": ["exact", "regex"], "dim": ["exact"]}
