from django.forms import NumberInput, Select, NullBooleanSelect, TextInput
from django.db.models import F, Case, When, Value
from django.db.models.fields import FloatField

from django_filters import rest_framework as filters
from histogram_file_manager.models import HistogramDataFile


class HistogramDataFileFilter(filters.FilterSet):

    id = filters.NumberFilter(
        field_name="id",
        widget=NumberInput(attrs={"class": "form-control"}),
    )
    entries_total__gt = filters.NumberFilter(
        field_name="entries_total",
        lookup_expr="gt",
        widget=NumberInput(attrs={"class": "form-control"}),
    )

    entries_total__lt = filters.NumberFilter(
        field_name="entries_total",
        lookup_expr="lt",
        widget=NumberInput(attrs={"class": "form-control"}),
    )

    processing_complete = filters.BooleanFilter(
        label="Processing complete",
        method="filter_processing_complete",
        widget=NullBooleanSelect(attrs={"class": "form-control"}),
    )

    filepath__contains = filters.CharFilter(
        field_name="filepath",
        lookup_expr="icontains",
        widget=TextInput(attrs={"class": "form-control"}),
    )

    data_era = filters.CharFilter(
        field_name="data_era",
        widget=TextInput(attrs={"class": "form-control"}),
    )

    data_dimensionality = filters.ChoiceFilter(
        choices=HistogramDataFile.HISTOGRAM_DIMENSIONS_CHOICES,
        field_name="contents__data_dimensionality",
        widget=Select(attrs={"class": "form-control"}),
    )

    granularity = filters.ChoiceFilter(
        choices=HistogramDataFile.DATAFILE_GRANULARITY_CHOICES,
        field_name="contents__granularity",
        widget=Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    def filter_processing_complete(self, queryset, name, value):
        """
        Custom filter for keeping only completely processed or unprocessed files

        Annotates the queryset with a percentage_complete field (differs
        from the one defined as a method in the model, which cannot be used
        directly into the query), so that we can get only processed/non-processed files.
        Takes care of not dividing by zero (entries_total = 0)
        """

        queryset = queryset.annotate(
            percentage_complete=Case(
                When(
                    entries_total__gt=0,
                    then=100 * F("entries_processed") / F("entries_total"),
                ),
                output_field=FloatField(),
                default=Value(0.0),
            )
        )

        # Requested processed files
        if value:
            return queryset.filter(percentage_complete__gte=100)
        # Requested unprocessed files
        else:
            return queryset.filter(percentage_complete__lt=100)

    class Meta:
        model = HistogramDataFile
        fields = [
            "id",
            "data_era",
            "data_dimensionality",
            "granularity",
            "processing_complete",
        ]
