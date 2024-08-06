from rest_framework import serializers

from .models import MLModelsIndex


class MLModelsIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModelsIndex
        fields = "__all__"
