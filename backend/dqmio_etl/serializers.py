from rest_framework import serializers

from .models import (
    Lumisection,
    LumisectionHistogram1D,
    LumisectionHistogram1DMEs,
    LumisectionHistogram2D,
    LumisectionHistogram2DMEs,
    Run,
)


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"


class LumisectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lumisection
        fields = "__all__"


class LumisectionHistogram1DMEsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionHistogram1DMEs
        fields = "__all__"


class LumisectionHistogram1DSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionHistogram1D
        fields = "__all__"


class LumisectionHistogram2DMEsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionHistogram2DMEs
        fields = "__all__"


class LumisectionHistogram2DSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionHistogram2D
        fields = "__all__"
