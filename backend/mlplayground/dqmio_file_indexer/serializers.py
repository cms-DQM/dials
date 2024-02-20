from rest_framework import serializers

from .models import BadFileIndex, FileIndex


class FileIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileIndex
        fields = "__all__"


class BadFileIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadFileIndex
        fields = "__all__"
