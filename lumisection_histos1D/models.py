from django.db import models
from runs.models import Run
from lumisections.models import Lumisection


# Create your models here.
class LumisectionHisto1D(models.Model):
    run_number = models.ForeignKey(Run, on_delete=models.CASCADE)
    ls_number  = models.ForeignKey(Lumisection, on_delete=models.CASCADE)

    date       = models.DateTimeField(auto_now_add=True)

    title      = models.CharField(max_length=30)
    data       = models.FloatField(blank=True)
    # ArrayField( ArrayField( models.IntegerField(blank=True), size=XX, ), size=XX,)
    entries    = models.IntegerField(blank=True, null=True)
    x_min      = models.FloatField(blank=True, null=True)
    x_max      = models.FloatField(blank=True, null=True)
    x_bin      = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"run {self.ls_number.run_number} / lumisection {self.ls_number.ls_number} / name {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['run_number', 'ls_number', 'title'], name='unique run / ls / 1d histogram combination')
        ]
