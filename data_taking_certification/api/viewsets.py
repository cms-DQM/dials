from rest_framework import viewsets

from data_taking_certification.models import RunCertification, LumisectionCertification
from data_taking_certification.api.serializers import (
    RunCertificationSerializer,
    LumisectionCertificationSerializer,
)
from data_taking_certification.api.filters import (
    RunCertificationFilter,
    LumisectionCertificationFilter,
)


class RunCertificationViewSet(viewsets.ModelViewSet):
    queryset = RunCertification.objects.all()
    serializer_class = RunCertificationSerializer
    filterset_class = RunCertificationFilter


class LumisectionCertificationViewSet(viewsets.ModelViewSet):
    queryset = LumisectionCertification.objects.all()
    serializer_class = LumisectionCertificationSerializer
    filterset_class = LumisectionCertificationFilter
