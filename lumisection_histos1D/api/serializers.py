from rest_framework import serializers
from lumisection_histos1D.models import LumisectionHisto1D


class LumisectionHisto1DSerializer(serializers.ModelSerializer):
    run = serializers.IntegerField(source="lumisection.run.run_number",
                                   read_only=True)
    lumisection = serializers.IntegerField(source="lumisection.ls_number",
                                           read_only=True)

    class Meta:
        model = LumisectionHisto1D
        exclude = ["date"]
