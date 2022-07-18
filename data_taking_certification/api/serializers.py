from rest_framework import serializers
from data_taking_objects.models import Run, Lumisection
from data_taking_certification.models import RunCertification, LumisectionCertification


class RunCertificationSerializer(serializers.ModelSerializer):
    run = serializers.IntegerField(source="run.run_number", read_only=True)

    class Meta:
        model = RunCertification
        fields = "__all__"


class LumisectionCertificationSerializer(serializers.ModelSerializer):
    run = serializers.IntegerField(source="lumisection.run.run_number", read_only=True)
    lumisection = serializers.IntegerField(
        source="lumisection.ls_number", read_only=True
    )

    class Meta:
        model = LumisectionCertification
        fields = "__all__"
