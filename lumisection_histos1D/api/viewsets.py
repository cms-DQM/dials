import logging
from rest_framework import viewsets
from lumisection_histos1D.models import LumisectionHisto1D
from lumisection_histos1D.api.serializers import LumisectionHisto1DSerializer
from lumisection_histos1D.api.filters import LumisectionHistos1DFilter

logger = logging.getLogger(__name__)


class LumisectionHisto1DViewset(viewsets.ModelViewSet):
    queryset = LumisectionHisto1D.objects.all()
    serializer_class = LumisectionHisto1DSerializer
    filterset_class = LumisectionHistos1DFilter
