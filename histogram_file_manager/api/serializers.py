import time
import logging
from rest_framework import serializers
from histogram_file_manager.models import HistogramDataFile

logger = logging.getLogger(__name__)


class HistogramDataFileSerializer(serializers.ModelSerializer):
    percentage_processed = serializers.DecimalField(max_digits=10,
                                                    decimal_places=1)

    def to_representation(self, instance, *args, **kwargs):
        # start = time.time()
        a = super().to_representation(instance, *args, **kwargs)
        # logger.debug(f"Serialization took {time.time() - start:.6f}")
        return a

    class Meta:
        model = HistogramDataFile
        fields = [
            'id', 'filepath', 'filesize', 'data_dimensionality', 'data_era',
            'entries_total', 'entries_processed', 'percentage_processed',
            'granularity', 'created', 'modified'
        ]


class HistogramDataFileSerializer_(serializers.Serializer):
    id = serializers.IntegerField()
    filepath = serializers.CharField()
    filesize = serializers.FloatField()
    data_dimensionality = serializers.IntegerField()
    data_era = serializers.CharField()
    entries_total = serializers.IntegerField()
    entries_processed = serializers.IntegerField()
    granularity = serializers.CharField()
    created = serializers.DateTimeField()
    modified = serializers.DateTimeField()
    percentage_processed = serializers.DecimalField(max_digits=10,
                                                    decimal_places=1)
