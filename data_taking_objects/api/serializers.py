from rest_framework import serializers
from data_taking_objects.models import Run


class RunSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Run
        fields = ('run_number', 'date')
