from rest_framework import serializers

from .models import Run


class RunSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Run
        fields = ('run_number', 'date')
