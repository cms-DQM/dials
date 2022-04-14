from django_filters import rest_framework as filters
from histogram_file_manager.models import HistogramDataFile


class HistogramDataFileFilter(filters.FilterSet):

    entries_total__gt = filters.NumberFilter(field_name='entries_total',
                                             lookup_expr='gt')

    entries_total__lt = filters.NumberFilter(field_name='entries_total',
                                             lookup_expr='lt')

    percentage_processed__gt = filters.NumberFilter(
        method="percentage_processed__gt",
        label="Percentage processed is greater than")

    percentage_processed__lt = filters.NumberFilter(
        method="percentage_processed__lt",
        label="Percentage processed is less than")

    def percentage_processed__gt(self, queryset, name, value):
        print("!!!!!!!!!!", queryset, name, value)
        return queryset

    def percentage_processed__lt(self, queryset, name, value):
        return queryset

    class Meta:
        model = HistogramDataFile
        fields = [
            'data_era',
            'data_dimensionality',
            'granularity',
        ]
