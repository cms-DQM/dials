from rest_framework import serializers
from utils.serializers_mixins import DatasetNameMixin

from .models import Lumisection


class LumisectionSerializer(DatasetNameMixin, serializers.ModelSerializer):
    class Meta:
        model = Lumisection
        fields = "__all__"
