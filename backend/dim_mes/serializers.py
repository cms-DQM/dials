from rest_framework import serializers
from utils.serializers_mixins import FieldsFilterMixin

from .models import MEs


class MEsSerializer(FieldsFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = MEs
        fields = "__all__"
