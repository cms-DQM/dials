import django_filters
from django import forms
from lumisection_histos1D.models import LumisectionHisto1D


class InFilter(django_filters.filters.BaseInFilter,
               django_filters.filters.CharFilter):
    pass
