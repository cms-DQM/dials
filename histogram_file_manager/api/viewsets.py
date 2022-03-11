import logging
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.api.serializers import HistogramDataFileSerializer

logger = logging.getLogger(__name__)


class HistogramDataFileViewset(viewsets.ModelViewSet):
    queryset = HistogramDataFile.objects.all()
    serializer_class = HistogramDataFileSerializer

    @action(detail=True, methods=['post'])
    def start_parsing(self, request, pk=None):
        """
        Start parsing a specific HistogramDataFile, identified by pk
        """
        required_params = ['granularity', 'data_dimensionality', 'data_format']
        hdf = self.get_object()  # Get specific HistogramDataFile

        if hdf.percentage_processed >= 100.0:
            return Response(
                f"HistogramDataFile with pk {pk} is already parsed",
                status=status.HTTP_400_BAD_REQUEST)
        elif any(param not in request.data for param in required_params):
            return Response(f"Required param(s) missing ({required_params})",
                            status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Requested parsing of {self.get_object()}")
        # Decide how the parsing will take place
        return Response(status=status.HTTP_202_ACCEPTED)
