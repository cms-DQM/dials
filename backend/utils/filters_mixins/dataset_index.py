from dataset_index.models import DatasetIndex
from django_filters import rest_framework as filters


class DatasetFilterMethods(filters.FilterSet):
    dataset = filters.CharFilter(method="exact_filter_dataset_index")
    dataset__regex = filters.CharFilter(method="regex_filter_dataset_index")

    def exact_filter_dataset_index(self, queryset, name, value):
        dataset_ids: list[int] = list(
            DatasetIndex.objects.using(queryset.db)
            .filter(dataset=value)
            .values_list(DatasetIndex.dataset_id.field.name, flat=True)
        )
        return queryset.filter(dataset_id__in=dataset_ids)

    def regex_filter_dataset_index(self, queryset, name, value):
        dataset_ids: list[int] = list(
            DatasetIndex.objects.using(queryset.db)
            .filter(dataset__regex=value)
            .values_list(DatasetIndex.dataset_id.field.name, flat=True)
        )
        return queryset.filter(dataset_id__in=dataset_ids)
