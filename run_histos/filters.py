import django_filters
from django import forms
from django.db import models
from run_histos.models import RunHisto


class InFilter(django_filters.filters.BaseInFilter, django_filters.filters.CharFilter):
    pass


class RunHistos1DFilter(django_filters.FilterSet):

    title = django_filters.filters.AllValuesMultipleFilter(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '10',
        })
    )

    primary_dataset = django_filters.AllValuesFilter(
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    run__run_number__in = InFilter(field_name='run__run_number', lookup_expr='in')

    class Meta:
        model = RunHisto
        fields = {
            'run__run_number': ['gte', 'lte',],
            'entries': ['gte', 'lte',],
            'mean': ['gte', 'lte',],
            'rms': ['gte', 'lte',],
            'skewness': ['gte', 'lte',],
            'kurtosis': ['gte', 'lte',],
        }
