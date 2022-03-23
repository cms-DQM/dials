import logging
from rest_framework import viewsets
from lumisection_histos2D.models import LumisectionHisto2D
from lumisection_histos2D.api.serializers import LumisectionHisto2DSerializer
from lumisection_histos2D.api.filters import LumisectionHisto2DFilter

logger = logging.getLogger(__name__)


class LumisectionHisto2DViewset(viewsets.ModelViewSet):
    queryset = LumisectionHisto2D.objects.all()
    serializer_class = LumisectionHisto2DSerializer
    filterset_class = LumisectionHisto2DFilter
