from django_filters import rest_framework as filters

from .models import BadFileIndex, FileIndex, FileIndexStatus


class FileIndexFilter(filters.FilterSet):
    path_contains = filters.CharFilter(label="File path contains", field_name="file_path", lookup_expr="contains")
    era = filters.CharFilter(label="Data era", field_name="data_era", lookup_expr="exact")
    min_size = filters.NumberFilter(label="Minimum file size", field_name="st_size", lookup_expr="gte")
    status = filters.ChoiceFilter(
        label="File contents ingestion status",
        field_name="status",
        lookup_expr="exact",
        choices=[(v, v) for v in FileIndexStatus.all()],
    )

    class Meta:
        model = FileIndex
        fields = ["path_contains", "era", "min_size", "status"]


class BadFileIndexFilter(filters.FilterSet):
    path_contains = filters.CharFilter(label="File path contains", field_name="file_path", lookup_expr="contains")
    era = filters.CharFilter(label="Data era", field_name="data_era", lookup_expr="exact")
    min_size = filters.NumberFilter(label="Minimum file size", field_name="st_size", lookup_expr="gte")

    class Meta:
        model = BadFileIndex
        fields = ["path_contains", "era", "min_size"]
