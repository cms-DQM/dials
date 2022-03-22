from lumisections.models import Lumisection
from rest_framework import serializers
from lumisection_histos2D.models import LumisectionHisto2D

class LumisectionHisto2DSerializer(serializers.ModelSerializer):
    run = serializers.IntegerField(source = 'lumisection.run.run_number', read_only = True)
    lumisection = serializers.IntegerField(source = 'lumisection.ls_number', read_only = True)

    class Meta:
        model = LumisectionHisto2D
        exclude = ['date']