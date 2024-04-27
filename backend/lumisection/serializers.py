from rest_framework import serializers

from .models import Lumisection


class LumisectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lumisection
        fields = "__all__"
