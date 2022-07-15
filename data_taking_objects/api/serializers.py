from rest_framework import serializers
from data_taking_objects.models import Run, Lumisection


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ("run_number", "date")


class LumisectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lumisection
        fields = (
            "run",
            "ls_number",
            "date",
        )

