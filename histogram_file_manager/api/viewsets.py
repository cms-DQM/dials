import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.api.serializers import HistogramDataFileSerializer
from histograms.models import RunHistogram, LumisectionHistogram1D, LumisectionHistogram2D
from histogram_file_manager.forms import HistogramDataFileStartParsingForm

logger = logging.getLogger(__name__)

HISTOGRAM_PARSING_FUNCTIONS_MAP = {
    'csv': {
        1: {
            # 'run': RunHistogram.from_csv,  # Not implemented yet
            'lumisection': LumisectionHistogram1D.from_csv
        },
        2: {
            'lumisection': LumisectionHistogram2D.from_csv
        }
    }
}


class HistogramDataFileViewset(viewsets.ModelViewSet):
    queryset = HistogramDataFile.objects.all()
    serializer_class = HistogramDataFileSerializer

    # Cache results for 60 seconds
    @method_decorator(cache_page(60 * 1))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def start_parsing(self, request, pk=None):
        """
        Start parsing a specific HistogramDataFile, identified by pk
        """
        required_params = ['granularity', 'data_dimensionality', 'file_format']
        hdf = self.get_object()  # Get specific HistogramDataFile

        if hdf.percentage_processed >= 100.0:
            return Response(
                f"HistogramDataFile with pk {pk} is already parsed",
                status=status.HTTP_400_BAD_REQUEST)
        # elif any(param not in request.data for param in required_params):
        # return Response(f"Required param(s) missing ({required_params})",
        # status=status.HTTP_400_BAD_REQUEST)

        # file_format = request.data['file_format'].lower()
        # granularity = request.data['granularity']
        # data_dimensionality = int(request.data['data_dimensionality'])
        form = HistogramDataFileStartParsingForm(request.POST)
        if form.is_valid():
            logger.info("!!!!!!")
        else:
            return Response(f"Required param(s) missing ({required_params})",
                            status=status.HTTP_400_BAD_REQUEST)

        # logger.info(
        # f"Requested parsing of {self.get_object()} as {file_format}")

        # Use the HISTOGRAM_PARSING_FUNCTIONS_MAP to find the appropriate parsing method
        # HISTOGRAM_PARSING_FUNCTIONS_MAP[file_format][data_dimensionality][
        # granularity](self.get_object().filepath)

        return Response(status=status.HTTP_202_ACCEPTED)
