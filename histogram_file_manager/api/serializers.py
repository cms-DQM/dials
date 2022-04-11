from rest_framework import serializers
from histogram_file_manager.models import HistogramDataFile


class HistogramDataFileSerializer(serializers.ModelSerializer):
    # percentage_processed = serializers.DecimalField(max_digits=10,
    # decimal_places=1)

    class Meta:
        model = HistogramDataFile
        fields = '__all__'
