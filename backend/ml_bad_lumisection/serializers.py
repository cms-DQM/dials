from rest_framework import serializers

from .models import MLBadLumisection


class MLBadLumisectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLBadLumisection
        fields = "__all__"
