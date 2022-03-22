from lumisections.models import Lumisection
from rest_framework import serializers
from histograms.models import RunHistogram, LumisectionHistogram1D, LumisectionHistogram2D


class RunHistogramSerializer(serializers.ModelSerializer):
    run = serializers.IntegerField(source='run.run_number', read_only=True)

    class Meta:
        model = RunHistogram
        exclude = ['date', 'path']


class LumisectionHistogram1DSerializer(serializers.ModelSerializer):
    run = serializers.IntegerField(source="lumisection.run.run_number",
                                   read_only=True)
    lumisection = serializers.IntegerField(source="lumisection.ls_number",
                                           read_only=True)

    class Meta:
        model = LumisectionHistogram1D
        exclude = ["date"]


class LumisectionHistogram2DSerializer(serializers.ModelSerializer):
    run = serializers.IntegerField(source='lumisection.run.run_number',
                                   read_only=True)
    lumisection = serializers.IntegerField(source='lumisection.ls_number',
                                           read_only=True)

    class Meta:
        model = LumisectionHistogram2D
        exclude = ['date']
