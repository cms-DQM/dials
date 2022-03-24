from django.db import models
from data_taking_objects.models import Run, Lumisection


class RunCertification(models.Model):
    run = models.ForeignKey(Run,
                            on_delete=models.CASCADE,
                            related_name="certifications")
    date = models.DateTimeField(auto_now_add=True)

    # run registry
    rr_is_pixel_good = models.BooleanField(null=True)
    rr_is_strip_good = models.BooleanField(null=True)
    rr_is_ecal_good = models.BooleanField(null=True)
    rr_is_hcal_good = models.BooleanField(null=True)
    rr_is_dt_good = models.BooleanField(null=True)
    rr_is_csc_good = models.BooleanField(null=True)
    rr_is_tracking_good = models.BooleanField(null=True)
    rr_is_muon_good = models.BooleanField(null=True)
    rr_is_egamma_good = models.BooleanField(null=True)
    rr_is_tau_good = models.BooleanField(null=True)
    rr_is_jetmet_good = models.BooleanField(null=True)
    rr_is_btag_good = models.BooleanField(null=True)

    rr_frac_pixel_good = models.FloatField(null=True)
    rr_frac_strip_good = models.FloatField(null=True)
    rr_frac_ecal_good = models.FloatField(null=True)
    rr_frac_hcal_good = models.FloatField(null=True)
    rr_frac_dt_good = models.FloatField(null=True)
    rr_frac_csc_good = models.FloatField(null=True)
    rr_frac_tracking_good = models.FloatField(null=True)
    rr_frac_muon_good = models.FloatField(null=True)
    rr_frac_egamma_good = models.FloatField(null=True)
    rr_frac_tau_good = models.FloatField(null=True)
    rr_frac_jetmet_good = models.FloatField(null=True)
    rr_frac_btag_good = models.FloatField(null=True)

    # elogs?

    def __str__(self):
        return f"run: {self.run.run_number}"
