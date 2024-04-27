from rest_framework import serializers

from .models import TH2


class TH2Serializer(serializers.ModelSerializer):
    class Meta:
        model = TH2
        fields = "__all__"
