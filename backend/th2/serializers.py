from rest_framework import serializers
from utils.serializers_mixins import DatasetNameMixin, MENameMixin

from .models import TH2


class TH2Serializer(DatasetNameMixin, MENameMixin, serializers.ModelSerializer):
    class Meta:
        model = TH2
        fields = "__all__"
