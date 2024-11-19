from rest_framework import serializers
from utils.serializers_mixins import DatasetNameMixin, FieldsFilterMixin, MENameMixin

from .models import TH1


class TH1Serializer(DatasetNameMixin, MENameMixin, FieldsFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = TH1
        fields = "__all__"
