from django_filters import rest_framework as filters

from .models import (
    Run,
    Lumisection,
    LumisectionHistogram1D,
    LumisectionHistogram2D,
)


class RunFilter(filters.FilterSet):
    min_run_number = filters.NumberFilter(
        label="Minimum run number", field_name="run_id", lookup_expr="gte"
    )
    max_run_number = filters.NumberFilter(
        label="Maximum run number", field_name="run_id", lookup_expr="lte"
    )

    class Meta:
        model = Run
        fields = ["min_run_number", "max_run_number"]


class LumisectionFilter(filters.FilterSet):
    min_ls_number = filters.NumberFilter(
        label="Minimum lumisection number", field_name="ls_number", lookup_expr="gte"
    )
    max_ls_number = filters.NumberFilter(
        label="Maximum lumisection number", field_name="ls_number", lookup_expr="lte"
    )
    min_run_number = filters.NumberFilter(
        label="Minimum run number", field_name="run_id", lookup_expr="gte"
    )
    max_run_number = filters.NumberFilter(
        label="Maximum run number", field_name="run_id", lookup_expr="lte"
    )

    class Meta:
        model = Lumisection
        fields = ["min_ls_number", "max_ls_number", "min_run_number", "max_run_number"]


class LumisectionHistogram1DFilter(filters.FilterSet):
    title_contains = filters.CharFilter(
        label="Title contains", field_name="title", lookup_expr="contains"
    )
    lumisection_id = filters.CharFilter(
        label="Lumisection id", field_name="lumisection_id", lookup_expr="exact"
    )
    min_entries = filters.NumberFilter(
        label="Minimum number of entries", field_name="entries", lookup_expr="gte"
    )

    class Meta:
        model = LumisectionHistogram1D
        fields = ["title_contains", "lumisection_id", "min_entries"]


class LumisectionHistogram2DFilter(filters.FilterSet):
    title_contains = filters.CharFilter(
        label="Title contains", field_name="title", lookup_expr="contains"
    )
    lumisection_id = filters.CharFilter(
        label="Lumisection id", field_name="lumisection_id", lookup_expr="exact"
    )
    min_entries = filters.NumberFilter(
        label="Minimum number of entries", field_name="entries", lookup_expr="gte"
    )

    class Meta:
        model = LumisectionHistogram2D
        fields = ["title_contains", "lumisection_id", "min_entries"]
