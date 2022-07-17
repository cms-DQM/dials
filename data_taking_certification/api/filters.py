from django_filters import rest_framework as filters
from data_taking_certification.models import RunCertification, LumisectionCertification


class RunCertificationFilter(filters.FilterSet):
    class Meta:
        model = RunCertification
        fields = "__all__"


class LumisectionCertificationFilter(filters.FilterSet):
    run = filters.NumberFilter(field_name="run__run_number")

    class Meta:
        model = LumisectionCertification
        fields = "__all__"
