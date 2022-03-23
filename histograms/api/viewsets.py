import logging
from rest_framework import viewsets
from histograms.models import RunHistogram, LumisectionHistogram1D, LumisectionHistogram2D
from histograms.api.serializers import RunHistogramSerializer, LumisectionHistogram1DSerializer, LumisectionHistogram2DSerializer
from histograms.api.filters import RunHistogramFilter, LumisectionHistogram1DFilter, LumisectionHistogram2DFilter

logger = logging.getLogger(__name__)


class RunHistogramViewSet(viewsets.ModelViewSet):
    queryset = RunHistogram.objects.all()
    serializer_class = RunHistogramSerializer
    filterset_class = RunHistogramFilter


class LumisectionHistogram1DViewSet(viewsets.ModelViewSet):
    queryset = LumisectionHistogram1D.objects.all()
    serializer_class = LumisectionHistogram1DSerializer
    filterset_class = LumisectionHistogram1DFilter


class LumisectionHistogram2DViewSet(viewsets.ModelViewSet):
    queryset = LumisectionHistogram2D.objects.all()
    serializer_class = LumisectionHistogram2DSerializer
    filterset_class = LumisectionHistogram2DFilter
