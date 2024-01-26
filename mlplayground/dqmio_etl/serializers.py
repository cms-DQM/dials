from rest_framework import serializers

from .models import (
    Run,
    Lumisection,
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


class DQMIOLumisectionHistogram1DSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionHistogram1D
        fields = "__all__"


class DQMIOLumisectionHistogram2DSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionHistogram2D
        fields = "__all__"


class DQMIOLumisectionHistogramsIngetionInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
