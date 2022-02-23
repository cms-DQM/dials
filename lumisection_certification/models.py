from django.db import models
from runs.models import Run
from lumisections.models import Lumisection
from lumisection_histos1D.models import LumisectionHisto1D
from lumisection_histos2D.models import LumisectionHisto2D

# Create your models here.
class LumisectionCertification(models.Model):
    lumisection  = models.ForeignKey(Lumisection, on_delete=models.CASCADE)
    date       = models.DateTimeField(auto_now_add=True)

    # run registry
    rr_is_golden_json = models.BooleanField(null=True)
    rr_is_pixel_good = models.FloatField(null=True)
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

    def __str__(self):
        return f"run: {self.lumisection.run.run_number} / lumi: {self.lumisection.ls_number}"
