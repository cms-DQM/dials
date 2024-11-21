from rest_framework import serializers
from utils.serializers_mixins import FieldsFilterMixin

from .models import MLModelsIndex


class MLModelsIndexSerializer(FieldsFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = MLModelsIndex
        fields = "__all__"
