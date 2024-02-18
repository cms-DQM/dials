from rest_framework import serializers

from .models import FileIndex


class FileIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileIndex
        fields = "__all__"
