from rest_framework import serializers
from utils.serializers_mixins import FieldsFilterMixin

from .models import MLBadLumisection


class MLBadLumisectionSerializer(FieldsFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = MLBadLumisection
        fields = "__all__"
