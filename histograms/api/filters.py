import django_filters
from django import forms
from histograms.models import RunHistogram, LumisectionHistogram1D, LumisectionHistogram2D


class InFilter(django_filters.filters.BaseInFilter,
               django_filters.filters.CharFilter):
    pass


class RunHistogramFilter(django_filters.rest_framework.FilterSet):

    title = django_filters.filters.AllValuesMultipleFilter(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '10',
        }))

    primary_dataset = django_filters.AllValuesFilter(widget=forms.Select(
        attrs={
            'class': 'form-control',
        }))

    run__run_number__in = InFilter(field_name='run__run_number',
                                   lookup_expr='in')

    class Meta:
        model = RunHistogram
        fields = {
            'run__run_number': [
                'gte',
                'lte',
            ],
            'entries': [
                'gte',
                'lte',
            ],
            'mean': [
                'gte',
                'lte',
            ],
            'rms': [
                'gte',
                'lte',
            ],
            'skewness': [
                'gte',
                'lte',
            ],
            'kurtosis': [
                'gte',
                'lte',
            ],
        }


class LumisectionHistogram1DFilter(django_filters.FilterSet):

    title = django_filters.filters.AllValuesMultipleFilter(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '10',
        }))

    lumisection__ls_number__in = InFilter(field_name='lumisection__ls_number',
                                          lookup_expr='in')
    lumisection__run__run_number__in = InFilter(
        field_name='lumisection__run__run_number', lookup_expr='in')

    class Meta:
        model = LumisectionHistogram1D
        fields = {
            'lumisection__run__run_number': [
                'gte',
                'lte',
            ],
            'lumisection__ls_number': [
                'gte',
                'lte',
            ],
            'entries': [
                'gte',
                'lte',
            ],
        }


class LumisectionHistogram2DFilter(django_filters.FilterSet):

    title = django_filters.filters.AllValuesMultipleFilter(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '10',
        }))

    lumisection__ls_number__in = InFilter(field_name='lumisection__ls_number',
                                          lookup_expr='in')
    lumisection__run__run_number__in = InFilter(
        field_name='lumisection__run__run_number', lookup_expr='in')

    class Meta:
        model = LumisectionHistogram2D
        fields = {
            'lumisection__run__run_number': [
                'gte',
                'lte',
            ],
            'lumisection__ls_number': [
                'gte',
                'lte',
            ],
            'entries': [
                'gte',
                'lte',
            ],
        }
