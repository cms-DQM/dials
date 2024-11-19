from rest_framework import serializers
from utils.serializers_mixins import DatasetNameMixin, FieldsFilterMixin

from .models import Lumisection


class LumisectionSerializer(DatasetNameMixin, FieldsFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = Lumisection
        fields = "__all__"
