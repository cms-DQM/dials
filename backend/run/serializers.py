from rest_framework import serializers
from utils.serializers_mixins import DatasetNameMixin

from .models import Run


class RunSerializer(DatasetNameMixin, serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"
