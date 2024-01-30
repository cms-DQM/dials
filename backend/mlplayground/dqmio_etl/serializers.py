from rest_framework import serializers

from .models import Run, Lumisection, LumisectionHistogram1D, LumisectionHistogram2D


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"


class LumisectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lumisection
        fields = "__all__"


class LumisectionHistogram1DSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionHistogram1D
        fields = "__all__"


class LumisectionHistogram2DSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionHistogram2D
        fields = "__all__"


class LumisectionHistogramsIngetionInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class LumisectionHistogramsSubsystemCountSerializer(serializers.Serializer):
    subsystem = serializers.CharField()
    count = serializers.IntegerField()
