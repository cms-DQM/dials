from rest_framework import serializers
from utils.serializers_mixins import DatasetNameMixin

from .models import FileIndex


class FileIndexSerializer(DatasetNameMixin, serializers.ModelSerializer):
    class Meta:
        model = FileIndex
        fields = "__all__"
