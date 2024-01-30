from urllib.parse import quote

from django.contrib.postgres.fields import ArrayField
from django.db import models
from dqmio_file_indexer.models import FileIndex


class Run(models.Model):
    run_number = models.IntegerField(unique=True, primary_key=True)
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
        constraints = [models.UniqueConstraint(fields=["run_number"], name="unique run number")]


class Lumisection(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="lumisections")
    ls_number = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    oms_zerobias_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"run {self.run.run_number} / lumisection {self.ls_number}"

    class Meta:
        ordering = ["run__run_number", "ls_number"]
        constraints = [models.UniqueConstraint(fields=["run", "ls_number"], name="unique run/ls combination")]


class HistogramBase(models.Model):
    """
    Abstract Base model to be inherited from Run and Lumisection Histograms
    """

    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=220)
    source_data_file = models.ForeignKey(
        FileIndex,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Source data file that the specific Histogram was read from, if any",
        related_name="%(class)s",
    )

    def title_sanitised(self):
        return quote(self.title, safe="")

    class Meta:
        abstract = True


class LumisectionHistogramBase(HistogramBase):
    """
    Abstract Base model that both 1D and 2D Histograms inherit from.
    """

    lumisection = models.ForeignKey(
        Lumisection,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_histograms",
    )
    entries = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class LumisectionHistogram1D(LumisectionHistogramBase):
    """
    Model containing 1D Lumisection granularity-level data (histogram information)
    """

    data = ArrayField(models.FloatField(), blank=True)
    x_min = models.FloatField(blank=True, null=True)
    x_max = models.FloatField(blank=True, null=True)
    x_bin = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"run {self.lumisection.run.run_number} / lumisection {self.lumisection.ls_number} / name {self.title}"

    class Meta:
        verbose_name_plural = "Lumisection Histograms 1D"
        constraints = [
            models.UniqueConstraint(
                fields=["lumisection", "title"],
                name="unique run / ls / 1d histogram combination",
            )
        ]


class LumisectionHistogram2D(LumisectionHistogramBase):
    """
    Model containing 2D Lumisection granularity-level data (histogram information)
    """

    data = ArrayField(ArrayField(models.FloatField(), blank=True), blank=True)
    x_min = models.FloatField(blank=True, null=True)
    x_max = models.FloatField(blank=True, null=True)
    x_bin = models.IntegerField(blank=True, null=True)
    y_max = models.FloatField(blank=True, null=True)
    y_min = models.FloatField(blank=True, null=True)
    y_bin = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"run {self.lumisection.run.run_number} / lumisection {self.lumisection.ls_number} / name {self.title}"

    class Meta:
        verbose_name_plural = "Lumisection Histograms 2D"
        constraints = [
            models.UniqueConstraint(
                fields=["lumisection", "title"],
                name="unique run / ls / 2d histogram combination",
            )
        ]
