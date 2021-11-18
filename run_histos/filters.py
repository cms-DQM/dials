import django_filters
from django import forms
from django.db import models
from run_histos.models import RunHisto

class InFilter(django_filters.filters.BaseInFilter, django_filters.filters.CharFilter):
    pass

class RunHistosFilter1D(django_filters.FilterSet):

    run__run_number__in = InFilter(field_name='run__run_number', lookup_expr='in')

    class Meta:
        model = RunHisto
        fields = {
            'run__run_number': ['gte', 'lte', ],
        }