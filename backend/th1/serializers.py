from rest_framework import serializers

from .models import TH1


class TH1Serializer(serializers.ModelSerializer):
    class Meta:
        model = TH1
        fields = "__all__"
