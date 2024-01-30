from rest_framework import serializers

from .models import FileIndex


class FileIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileIndex
        fields = "__all__"


class FileIndexInputSerializer(serializers.Serializer): ...


class FileIndexResponseSerializer(serializers.Serializer):
    storage = serializers.CharField()
    total = serializers.IntegerField()
    added = serializers.IntegerField()
    ingested_ids = serializers.ListField(child=serializers.IntegerField())
