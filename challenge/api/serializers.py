from rest_framework import serializers
from challenge.models import Task, Strategy, Prediction
from data_taking_objects.api.serializers import RunSerializer, LumisectionSerializer
from histograms.api.serializers import (
    RunHistogramSerializer,
    LumisectionHistogram1DSerializer,
    LumisectionHistogram2DSerializer,
)


class TaskSerializer(serializers.ModelSerializer):
    training_runs = RunSerializer(many=True)
    testing_runs = RunSerializer(many=True)
    training_lumisections = LumisectionSerializer(many=True)
    testing_lumisections = LumisectionSerializer(many=True)

    class Meta:
        model = Task
        fields = "__all__"


class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = "__all__"


class PredictionSerializer(serializers.ModelSerializer):
    strategy = serializers.CharField(source="strategy.model")
    run_histograms = RunHistogramSerializer(many=True)
    lumisection_histograms_1d = LumisectionHistogram1DSerializer(many=True)
    lumisection_histograms_2d = LumisectionHistogram2DSerializer(many=True)

    class Meta:
        model = Prediction
        fields = "__all__"
