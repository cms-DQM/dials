from rest_framework import serializers
from utils.serializers_mixins import DatasetNameMixin, FieldsFilterMixin

from .models import Run


class RunSerializer(DatasetNameMixin, FieldsFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"
