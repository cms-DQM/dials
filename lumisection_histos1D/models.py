import json
import logging
import pandas as pd  # https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
from django.db import models
from django.contrib.postgres.fields import ArrayField
from runs.models import Run
from lumisections.models import Lumisection


# Create your models here.
class LumisectionHisto1D(models.Model):
    lumisection = models.ForeignKey(Lumisection, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=100)
    data = ArrayField(models.FloatField(), blank=True)
    entries = models.IntegerField(blank=True, null=True)
    x_min = models.FloatField(blank=True, null=True)
    x_max = models.FloatField(blank=True, null=True)
    x_bin = models.IntegerField(blank=True, null=True)

    @staticmethod
    def from_file(file_path):
        """
        Import 1D Lumisection Histogram from a filepath
        """
        df = pd.read_csv(file_path)
        logging.debug("Datafile head: {df.head()}")
        logging.debug("Datafile columns:\n {df.columns}")

        lumisection_histos1D = []
        count = 0

        for index, row in df.iterrows():
            run_number = row["fromrun"]
            lumi_number = row["fromlumi"]
            title = row["hname"]
            entries = row["entries"]
            data = json.loads(row["histo"])

            logging.debug(
                f"Run: {run_number}\tLumisection: {lumi_number}\tTitle: {title}"
            )

            run, _ = Run.objects.get_or_create(run_number=run_number)
            lumisection, _ = Lumisection.objects.get_or_create(
                run=run, ls_number=lumi_number)

            lumisection_histo1D = LumisectionHisto1D(lumisection=lumisection,
                                                     title=title,
                                                     entries=entries,
                                                     data=data)

            lumisection_histos1D.append(lumisection_histo1D)
            count += 1
            if count == 50:
                LumisectionHisto1D.objects.bulk_create(lumisection_histos1D,
                                                       ignore_conflicts=True)
                logging.info(
                    "50 lumisections 1D histograms successfully added!")
                count = 0
                lumisection_histos1D = []
        if lumisection_histos1D:
            LumisectionHisto1D.objects.bulk_create(lumisection_histos1D,
                                                   ignore_conflicts=True)

    def __str__(self):
        return f"run {self.lumisection.run.run_number} / lumisection {self.lumisection.ls_number} / name {self.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["lumisection", "title"],
                name="unique run / ls / 1d histogram combination",
            )
        ]
