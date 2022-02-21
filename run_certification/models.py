from django.db import models
from runs.models import Run
from run_histos.models import RunHisto


class RunCertification(models.Model):
    run        = models.ForeignKey(Run, on_delete=models.CASCADE)
    date       = models.DateTimeField(auto_now_add=True)

    # run registry
    rr_is_tracker_good = models.BooleanField(null=True)

    def __str__(self):
        return f"run: {self.run.run_number}"
