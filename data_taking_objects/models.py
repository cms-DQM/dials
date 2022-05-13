from django.db import models


class Run(models.Model):
    run_number = models.IntegerField(unique=True)
    run_date = models.DateTimeField(blank=True, null=True)

    year = models.IntegerField(blank=True, null=True)
    period = models.CharField(max_length=1, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    oms_fill = models.IntegerField(blank=True, null=True)
    oms_lumisections = models.IntegerField(blank=True, null=True)
    oms_initial_lumi = models.FloatField(blank=True, null=True)
    oms_end_lumi = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"run {self.run_number}"

    class Meta:
        ordering = ["run_number"]
        constraints = [
            models.UniqueConstraint(fields=["run_number"], name="unique run number")
        ]


class Lumisection(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="lumisections")
    ls_number = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    oms_zerobias_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"run {self.run.run_number} / lumisection {self.ls_number}"

    class Meta:
        ordering = ["run__run_number", "ls_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["run", "ls_number"], name="unique run/ls combination"
            )
        ]
