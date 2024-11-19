from rest_framework import serializers
from utils.serializers_mixins import DatasetNameMixin, FieldsFilterMixin

from .models import FileIndex


class FileIndexSerializer(DatasetNameMixin, FieldsFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = FileIndex
        fields = "__all__"
