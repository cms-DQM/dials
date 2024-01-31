from django_filters import rest_framework as filters

from .models import Lumisection, LumisectionHistogram1D, LumisectionHistogram2D, Run


class RunFilter(filters.FilterSet):
    min_run_number = filters.NumberFilter(label="Minimum run number", field_name="run_number", lookup_expr="gte")
    max_run_number = filters.NumberFilter(label="Maximum run number", field_name="run_number", lookup_expr="lte")

    class Meta:
        model = Run
        fields = ["min_run_number", "max_run_number"]


class LumisectionFilter(filters.FilterSet):
    run_number = filters.NumberFilter(label="Run number", field_name="run__run_number", lookup_expr="exact")
    min_ls_number = filters.NumberFilter(label="Minimum lumisection number", field_name="ls_number", lookup_expr="gte")
    max_ls_number = filters.NumberFilter(label="Maximum lumisection number", field_name="ls_number", lookup_expr="lte")
    min_run_number = filters.NumberFilter(label="Minimum run number", field_name="run_id", lookup_expr="gte")
    max_run_number = filters.NumberFilter(label="Maximum run number", field_name="run_id", lookup_expr="lte")

    class Meta:
        model = Lumisection
        fields = ["run_number", "min_ls_number", "max_ls_number", "min_run_number", "max_run_number"]


class LumisectionHistogram1DFilter(filters.FilterSet):
    run_number = filters.NumberFilter(label="Run number", field_name="lumisection__run", lookup_expr="exact")
    ls_number = filters.NumberFilter(
        label="Lumisection number", field_name="lumisection__ls_number", lookup_expr="exact"
    )
    min_run_number = filters.NumberFilter(label="Minimum run number", field_name="lumisection__run", lookup_expr="gte")
    max_run_number = filters.NumberFilter(label="Maximum run number", field_name="lumisection__run", lookup_expr="lte")
    min_ls_number = filters.NumberFilter(
        label="Minimum lumisection number", field_name="lumisection__ls_number", lookup_expr="gte"
    )
    max_ls_number = filters.NumberFilter(
        label="Maximum lumisection number", field_name="lumisection__ls_number", lookup_expr="lte"
    )
    title_contains = filters.CharFilter(label="Title contains", field_name="title", lookup_expr="contains")
    min_entries = filters.NumberFilter(label="Minimum number of entries", field_name="entries", lookup_expr="gte")

    class Meta:
        model = LumisectionHistogram1D
        fields = ["run_number", "ls_number", "title_contains", "lumisection_id", "min_entries"]


class LumisectionHistogram2DFilter(filters.FilterSet):
    run_number = filters.NumberFilter(label="Run number", field_name="lumisection__run", lookup_expr="exact")
    ls_number = filters.NumberFilter(
        label="Lumisection number", field_name="lumisection__ls_number", lookup_expr="exact"
    )
    min_run_number = filters.NumberFilter(label="Minimum run number", field_name="lumisection__run", lookup_expr="gte")
    max_run_number = filters.NumberFilter(label="Maximum run number", field_name="lumisection__run", lookup_expr="lte")
    min_ls_number = filters.NumberFilter(
        label="Minimum lumisection number", field_name="lumisection__ls_number", lookup_expr="gte"
    )
    max_ls_number = filters.NumberFilter(
        label="Maximum lumisection number", field_name="lumisection__ls_number", lookup_expr="lte"
    )
    title_contains = filters.CharFilter(label="Title contains", field_name="title", lookup_expr="contains")
    min_entries = filters.NumberFilter(label="Minimum number of entries", field_name="entries", lookup_expr="gte")

    class Meta:
        model = LumisectionHistogram2D
        fields = ["run_number", "ls_number", "title_contains", "lumisection_id", "min_entries"]
