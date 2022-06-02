from rest_framework import viewsets

from data_taking_objects.models import Run, Lumisection
from data_taking_objects.api.serializers import RunSerializer, LumisectionSerializer
from data_taking_objects.api.filters import RunFilter, LumisectionFilter


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    filterset_class = RunFilter


class LumisectionViewSet(viewsets.ModelViewSet):
    queryset = Lumisection.objects.all()
    serializer_class = LumisectionSerializer
    filterset_class = LumisectionFilter
