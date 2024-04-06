from typing import ClassVar

from django.db.models import Q
from django_filters import rest_framework as filters
from utils.validators import validate_th_filterset

from .models import Lumisection, LumisectionHistogram1D, LumisectionHistogram2D, Run


class RunFilter(filters.FilterSet):
    min_run_number = filters.NumberFilter(label="Minimum run number", field_name="run_number", lookup_expr="gte")
    max_run_number = filters.NumberFilter(label="Maximum run number", field_name="run_number", lookup_expr="lte")

    class Meta:
        model = Run
        fields: ClassVar[list[str]] = ["min_run_number", "max_run_number"]


class LumisectionFilter(filters.FilterSet):
    min_ls_number = filters.NumberFilter(label="Minimum lumisection number", field_name="ls_number", lookup_expr="gte")
    max_ls_number = filters.NumberFilter(label="Maximum lumisection number", field_name="ls_number", lookup_expr="lte")
    run_number = filters.NumberFilter(label="Run number", method="filter_by_run_number")

    class Meta:
        model = Lumisection
        fields: ClassVar[list[str]] = [
            "run_number",
            "ls_number",
            "min_ls_number",
            "max_ls_number",
        ]

    def filter_by_run_number(self, queryset, name, value):
        return queryset.filter(
            Q(lumisectionhistogram1d__run_number=value) | Q(lumisectionhistogram2d__run_number=value)
        )


class LumisectionHistogram1DFilter(filters.FilterSet):
    ls_number = filters.NumberFilter(label="Lumisection number", field_name="ls_id__ls_number", lookup_expr="exact")
    min_run_number = filters.NumberFilter(label="Minimum run number", field_name="run_number", lookup_expr="gte")
    max_run_number = filters.NumberFilter(label="Maximum run number", field_name="run_number", lookup_expr="lte")
    min_ls_number = filters.NumberFilter(
        label="Minimum lumisection number", field_name="ls_id__ls_number", lookup_expr="gte"
    )
    max_ls_number = filters.NumberFilter(
        label="Maximum lumisection number", field_name="ls_id__ls_number", lookup_expr="lte"
    )
    title_contains = filters.CharFilter(label="Title contains", field_name="title", lookup_expr="contains")
    min_entries = filters.NumberFilter(label="Minimum number of entries", field_name="entries", lookup_expr="gte")
    era = filters.CharFilter(label="Data era", field_name="file_id__era", lookup_expr="exact")
    campaign = filters.CharFilter(label="Campaign", field_name="file_id__campaign", lookup_expr="contains")
    dataset = filters.CharFilter(label="Dataset", field_name="file_id__dataset", lookup_expr="contains")

    def filter_queryset(self, queryset, *args, **kwargs):
        queryset = super().filter_queryset(queryset, *args, **kwargs)
        validate_th_filterset(self.form)
        return queryset

    class Meta:
        model = LumisectionHistogram1D
        fields: ClassVar[list[str]] = [
            "run_number",
            "ls_number",
            "ls_id",
            "title",
            "min_run_number",
            "max_run_number",
            "min_ls_number",
            "max_ls_number",
            "title_contains",
            "min_entries",
            "era",
            "campaign",
            "dataset",
        ]


class LumisectionHistogram2DFilter(filters.FilterSet):
    ls_number = filters.NumberFilter(label="Lumisection number", field_name="ls_id__ls_number", lookup_expr="exact")
    min_run_number = filters.NumberFilter(label="Minimum run number", field_name="run_number", lookup_expr="gte")
    max_run_number = filters.NumberFilter(label="Maximum run number", field_name="run_number", lookup_expr="lte")
    min_ls_number = filters.NumberFilter(
        label="Minimum lumisection number", field_name="ls_id__ls_number", lookup_expr="gte"
    )
    max_ls_number = filters.NumberFilter(
        label="Maximum lumisection number", field_name="ls_id__ls_number", lookup_expr="lte"
    )
    title_contains = filters.CharFilter(label="Title contains", field_name="title", lookup_expr="contains")
    min_entries = filters.NumberFilter(label="Minimum number of entries", field_name="entries", lookup_expr="gte")
    era = filters.CharFilter(label="Data era", field_name="file_id__era", lookup_expr="exact")
    campaign = filters.CharFilter(label="Campaign", field_name="file_id__campaign", lookup_expr="contains")
    dataset = filters.CharFilter(label="Dataset", field_name="file_id__dataset", lookup_expr="contains")

    def filter_queryset(self, queryset, *args, **kwargs):
        queryset = super().filter_queryset(queryset, *args, **kwargs)
        validate_th_filterset(self.form)
        return queryset

    class Meta:
        model = LumisectionHistogram2D
        fields: ClassVar[list[str]] = [
            "run_number",
            "ls_number",
            "ls_id",
            "title",
            "min_run_number",
            "max_run_number",
            "min_ls_number",
            "max_ls_number",
            "title_contains",
            "min_entries",
            "era",
            "campaign",
            "dataset",
        ]
