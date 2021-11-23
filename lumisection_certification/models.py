from django.db import models
from runs.models import Run
from lumisections.models import Lumisection
from lumisection_histos1D.models import LumisectionHisto1D
from lumisection_histos2D.models import LumisectionHisto2D

# Create your models here.
class LumisectionCertification(models.Model):
    lumisection  = models.ForeignKey(Lumisection, on_delete=models.CASCADE)
    date       = models.DateTimeField(auto_now_add=True)

    # pca
    pca_1      = models.FloatField(null=True)
    pca_2      = models.FloatField(null=True)

    def __str__(self):
        return f"run: {self.lumisection.run.run_number} / lumi: {self.lumisection.ls_number}"
