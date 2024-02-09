from rest_framework import serializers

from .models import FileIndex


class FileIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileIndex
        fields = "__all__"


class FileIndexResponseSerializer(serializers.Serializer):
    storage = serializers.CharField()
    total = serializers.IntegerField()
    added_good = serializers.IntegerField()
    added_bad = serializers.IntegerField()
    good_ingested_ids = serializers.ListField(child=serializers.IntegerField())
    bad_ingested_ids = serializers.ListField(child=serializers.IntegerField())
