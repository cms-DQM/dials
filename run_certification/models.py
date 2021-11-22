from django.db import models
from runs.models import Run
from run_histos.models import RunHisto

# Create your models here.
class RunCertification(models.Model):
    run_number = models.ForeignKey(Run, on_delete=models.CASCADE)
    date       = models.DateTimeField(auto_now_add=True)

    # pca
    pca_1      = models.FloatField(null=True)
    pca_2      = models.FloatField(null=True)

    def __str__(self):
        return f"run: {self.run_number.run_number}"


