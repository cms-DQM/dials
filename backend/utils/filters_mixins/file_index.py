from django_filters import rest_framework as filters
from file_index.models import FileIndex


class FileIndexMethods(filters.FilterSet):
    logical_file_name = filters.CharFilter(method="exact_filter_logical_file_name")
    logical_file_name__regex = filters.CharFilter(method="regex_filter_logical_file_name")

    def exact_filter_logical_file_name(self, queryset, name, value):
        file_ids: list[int] = list(
            FileIndex.objects.using(queryset.db)
            .filter(logical_file_name=value)
            .values_list(FileIndex.file_id.field.name, flat=True)
        )
        return queryset.filter(file_id__in=file_ids)

    def regex_filter_logical_file_name(self, queryset, name, value):
        file_ids: list[int] = list(
            FileIndex.objects.using(queryset.db)
            .filter(logical_file_name__regex=value)
            .values_list(FileIndex.file_id.field.name, flat=True)
        )
        return queryset.filter(file_id__in=file_ids)
