from rest_framework import serializers

from .models import MEs


class MEsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MEs
        fields = "__all__"


class MinifiedMEsSerializer(MEsSerializer):
    class Meta:
        model = MEs
        fields = ("me_id", "me", "dim")
