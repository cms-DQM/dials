from rest_framework import serializers
from run_histos.models import RunHisto

class RunHistosSerializer(serializers.ModelSerializer):
    run = serializers.IntegerField(source = 'run.run_number', read_only = True)

    class Meta:
        model = RunHisto
        exclude = ['date', 'path']
    