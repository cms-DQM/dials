from django.db import models
from runs.models import Run

# Create your models here.
class Lumisection(models.Model):
    run_number = models.ForeignKey(Run, on_delete=models.CASCADE)
    ls_number  = models.IntegerField()
    date       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"run {self.run_number.run_number} / lumisection {self.ls_number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['run_number', 'ls_number'], name='unique run/ls combination')
        ]
