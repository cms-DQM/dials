from rest_framework import serializers

from .models import DatasetIndex


class DatasetIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetIndex
        fields = "__all__"
