from rest_framework import serializers
from utils.serializers_mixins import DatasetNameMixin, FieldsFilterMixin, MENameMixin

from .models import TH2


class TH2Serializer(DatasetNameMixin, MENameMixin, FieldsFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = TH2
        fields = "__all__"
