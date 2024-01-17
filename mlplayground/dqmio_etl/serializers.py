from rest_framework import serializers

from .models import (
    Run,
    Lumisection,
    RunHistogram,
    LumisectionHistogram1D,
    LumisectionHistogram2D
)


class DQMIORunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"


class DQMIOLumisectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lumisection
        fields = "__all__"


class DQMIORunHistogramSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunHistogram
        fields = "__all__"


class DQMIOLumisectionHistogram1DSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionHistogram1D
        fields = "__all__"


class DQMIOLumisectionHistogram1DInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class DQMIOLumisectionHistogram2DSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionHistogram2D
        fields = "__all__"


class DQMIOLumisectionHistogram2DInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    readUntilLumi = serializers.IntegerField(default=-1)


class DQMIOLumisectionHistogramResponseSerializer(serializers.Serializer):
    entries_ingested = serializers.IntegerField()
