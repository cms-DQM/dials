from django.db import models
from runs.models import Run

# Create your models here.
class Lumisection(models.Model):
    run        = models.ForeignKey(Run, on_delete=models.CASCADE)
    ls_number  = models.IntegerField()
    date       = models.DateTimeField(auto_now_add=True)

    oms_zerobias_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"run {self.run.run_number} / lumisection {self.ls_number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['run', 'ls_number'], name='unique run/ls combination')
        ]
