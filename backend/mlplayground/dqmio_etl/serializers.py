from rest_framework import serializers

from .models import Lumisection, LumisectionHistogram1D, LumisectionHistogram2D, Run


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"


class LumisectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lumisection
        fields = "__all__"


class LumisectionHistogram1DSerializer(serializers.ModelSerializer):
    ls_number = serializers.IntegerField(source="lumisection.ls_number")
    run_number = serializers.IntegerField(source="lumisection.run.run_number")

    class Meta:
        model = LumisectionHistogram1D
        fields = "__all__"


class LumisectionHistogram2DSerializer(serializers.ModelSerializer):
    ls_number = serializers.IntegerField(source="lumisection.ls_number")
    run_number = serializers.IntegerField(source="lumisection.run.run_number")

    class Meta:
        model = LumisectionHistogram2D
        fields = "__all__"


class LumisectionHistogramsIngetionInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class LumisectionHistogramsSubsystemCountSerializer(serializers.Serializer):
    subsystem = serializers.CharField()
    count = serializers.IntegerField()
