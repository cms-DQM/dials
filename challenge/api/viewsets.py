from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from challenge.models import Task, Strategy, Prediction
from challenge.api.serializers import (
    TaskSerializer,
    StrategySerializer,
    PredictionSerializer,
)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer


class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
