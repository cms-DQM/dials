from rest_framework import serializers

from .models import Lumisection, LumisectionHistogram1D, LumisectionHistogram2D, Run


class ExtraFieldsSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ExtraFieldsSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, "extra_fields", None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"


class LumisectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lumisection
        fields = "__all__"


class LumisectionHistogram1DSerializer(ExtraFieldsSerializer):
    ls_number = serializers.IntegerField(source="lumisection.ls_number")
    run_number = serializers.IntegerField(source="lumisection.run.run_number")

    class Meta:
        model = LumisectionHistogram1D
        fields = "__all__"
        extra_fields = ["ls_number", "run_number"]


class LumisectionHistogram2DSerializer(ExtraFieldsSerializer):
    ls_number = serializers.IntegerField(source="lumisection.ls_number")
    run_number = serializers.IntegerField(source="lumisection.run.run_number")

    class Meta:
        model = LumisectionHistogram2D
        fields = "__all__"
        extra_fields = ["ls_number", "run_number"]


class LumisectionHistogramsIngetionInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class LumisectionHistogramsSubsystemCountSerializer(serializers.Serializer):
    subsystem = serializers.CharField()
    count = serializers.IntegerField()
