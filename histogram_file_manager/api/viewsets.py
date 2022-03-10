from rest_framework import viewsets
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.api.serializers import HistogramDataFileSerializer


class HistogramDataFileViewset(viewsets.ModelViewSet):
    queryset = HistogramDataFile.objects.all()
    serializer_class = HistogramDataFileSerializer
