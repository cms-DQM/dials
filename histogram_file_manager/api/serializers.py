# import time
import logging
from rest_framework import serializers
from histogram_file_manager.models import HistogramDataFile, HistogramDataFileContents

logger = logging.getLogger(__name__)


class HistogramDataFileContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistogramDataFileContents
        fields = ["granularity", "data_dimensionality"]


class HistogramDataFileSerializer(serializers.ModelSerializer):
    run_histograms = serializers.IntegerField(
        source="runhistogram.count",
        help_text="Total Run Histograms retrieved form this file",
    )
    lumisection_histograms_1d = serializers.IntegerField(
        source="lumisectionhistogram1d.count",
        help_text="Total Lumisection 1D Histograms retrieved form this file",
    )
    lumisection_histograms_2d = serializers.IntegerField(
        source="lumisectionhistogram2d.count",
        help_text="Total Lumisection 2D Histograms retrieved form this file",
    )
    contents = HistogramDataFileContentsSerializer(
        many=True,
        help_text="The file's contents in regards to histogram type and dimensionality",
    )

    class Meta:
        model = HistogramDataFile
        fields = [
            "id",
            "filepath",
            "filesize",
            "data_era",
            "entries_total",
            "entries_processed",
            "percentage_processed",
            "contents",
            "created",
            "modified",
            "run_histograms",
            "lumisection_histograms_1d",
            "lumisection_histograms_2d",
        ]
