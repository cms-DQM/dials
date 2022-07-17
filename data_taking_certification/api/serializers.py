from rest_framework import serializers
from data_taking_certification.models import RunCertification, LumisectionCertification


class RunCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunCertification
        fields = (
            "run", 
            "rr_frac_pixel_good", 
            "rr_frac_strip_good", 
            "rr_frac_tracking_good"
        )


class LumisectionCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LumisectionCertification
        fields = (
            "run",
            "lumisection",
            "rr_is_pixel_good",
            "rr_is_strip_good",
            "rr_is_tracking_good"
        )
