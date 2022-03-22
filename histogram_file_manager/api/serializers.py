from rest_framework import serializers
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.forms import HistogramDataFileForm


class HistogramDataFileSerializer(serializers.ModelSerializer):
    percentage_processsed = serializers.FloatField(
        source="percentage_processed")

    class Meta:
        model = HistogramDataFile
        fields = '__all__'
