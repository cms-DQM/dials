from django_filters import rest_framework as filters
from data_taking_objects.models import Run, Lumisection


class RunFilter(filters.FilterSet):
    class Meta:
        model = Run
        fields = "__all__"


class LumisectionFilter(filters.FilterSet):
    class Meta:
        model = Lumisection
        fields = "__all__"
