from django_filters import rest_framework as filters
from rest_framework.exceptions import ParseError

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

    def filter_queryset(self, queryset, *args, **kwargs):
        queryset = super().filter_queryset(queryset, *args, **kwargs)
        cleaned_data = {key: value for key, value in self.form.cleaned_data.items() if value is not None}

        run_number_used = "run_number" in cleaned_data
        min_run_number_used = "min_run_number" in cleaned_data
        max_run_number_used = "max_run_number" in cleaned_data

        if run_number_used and (min_run_number_used or max_run_number_used):
            raise ParseError("run number and range run number filter cannot be used together.")

        return queryset

    class Meta:
        model = Lumisection
        fields = ["run_number", "ls_number", "min_ls_number", "max_ls_number", "min_run_number", "max_run_number"]


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

    def filter_queryset(self, queryset, *args, **kwargs):
        queryset = super().filter_queryset(queryset, *args, **kwargs)
        cleaned_data = {key: value for key, value in self.form.cleaned_data.items() if value is not None}

        run_number_used = "run_number" in cleaned_data
        min_run_number_used = "min_run_number" in cleaned_data
        max_run_number_used = "max_run_number" in cleaned_data

        if run_number_used and (min_run_number_used or max_run_number_used):
            raise ParseError("run number and range run number cannot be used together.")

        lumisection_id_used = "lumisection_id" in cleaned_data
        ls_number_used = "ls_number" in cleaned_data
        min_ls_number_used = "min_ls_number" in cleaned_data
        max_ls_number_used = "max_ls_number" in cleaned_data

        if ls_number_used and lumisection_id_used:
            raise ParseError("ls number and lumisection id cannot be used together.")

        if lumisection_id_used and (min_ls_number_used or max_ls_number_used):
            raise ParseError("lumisection id and range ls number cannot be used together.")

        if ls_number_used and (min_ls_number_used or max_ls_number_used):
            raise ParseError("ls number and range ls number cannot be used together.")

        title_used = "title" in cleaned_data
        title_contains_used = "title_contains" in cleaned_data

        if title_used and title_contains_used:
            raise ParseError("title and title contains cannot be used together.")

        return queryset

    class Meta:
        model = LumisectionHistogram1D
        fields = [
            "run_number",
            "ls_number",
            "lumisection_id",
            "title",
            "min_run_number",
            "max_run_number",
            "min_ls_number",
            "max_ls_number",
            "title_contains",
            "min_entries",
        ]


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

    def filter_queryset(self, queryset, *args, **kwargs):
        queryset = super().filter_queryset(queryset, *args, **kwargs)
        cleaned_data = {key: value for key, value in self.form.cleaned_data.items() if value is not None}

        run_number_used = "run_number" in cleaned_data
        min_run_number_used = "min_run_number" in cleaned_data
        max_run_number_used = "max_run_number" in cleaned_data

        if run_number_used and (min_run_number_used or max_run_number_used):
            raise ParseError("run number and range run number cannot be used together.")

        lumisection_id_used = "lumisection_id" in cleaned_data
        ls_number_used = "ls_number" in cleaned_data
        min_ls_number_used = "min_ls_number" in cleaned_data
        max_ls_number_used = "max_ls_number" in cleaned_data

        if ls_number_used and lumisection_id_used:
            raise ParseError("ls number and lumisection id cannot be used together.")

        if lumisection_id_used and (min_ls_number_used or max_ls_number_used):
            raise ParseError("lumisection id and range ls number cannot be used together.")

        if ls_number_used and (min_ls_number_used or max_ls_number_used):
            raise ParseError("ls number and range ls number cannot be used together.")

        title_used = "title" in cleaned_data
        title_contains_used = "title_contains" in cleaned_data

        if title_used and title_contains_used:
            raise ParseError("title and title contains cannot be used together.")

    class Meta:
        model = LumisectionHistogram2D
        fields = [
            "run_number",
            "ls_number",
            "lumisection_id",
            "title",
            "min_run_number",
            "max_run_number",
            "min_ls_number",
            "max_ls_number",
            "title_contains",
            "min_entries",
        ]
