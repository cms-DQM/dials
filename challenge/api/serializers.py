from rest_framework import serializers
from challenge.models import Task, Strategy, Prediction


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = "__all__"


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = "__all__"
