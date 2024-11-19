from rest_framework import serializers
from utils.serializers_mixins import FieldsFilterMixin

from .models import DatasetIndex


class DatasetIndexSerializer(FieldsFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = DatasetIndex
        fields = "__all__"
