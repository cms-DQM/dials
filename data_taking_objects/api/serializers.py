from rest_framework import serializers
from data_taking_objects.models import Run, Lumisection


class RunSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Run
        fields = ("run_number", "date")


class LumisectionSerializer(serializers.HyperlinkedModelSerializer):
    run = serializers.IntegerField(source="run.run_number")

    class Meta:
        model = Lumisection
        fields = ("run", "date")
