import os.path
import json
import logging
import pandas as pd  # https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
from django.db import models
from django.contrib.postgres.fields import ArrayField
from runs.models import Run
from lumisections.models import Lumisection
from histogram_file_manager.models import HistogramDataFile

logger = logging.getLogger(__name__)


class LumisectionHisto1D(models.Model):
    lumisection = models.ForeignKey(Lumisection, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=100)
    data = ArrayField(models.FloatField(), blank=True)
    entries = models.IntegerField(blank=True, null=True)
    x_min = models.FloatField(blank=True, null=True)
    x_max = models.FloatField(blank=True, null=True)
    x_bin = models.IntegerField(blank=True, null=True)
    source_data_file = models.ForeignKey(
        HistogramDataFile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=
        "Source data file that the specific Histogram was read from, if any")

    @staticmethod
    def from_file(file_path, data_era: str = ""):
        """
        Import 1D Lumisection Histograms from a filepath
        """
        df = pd.read_csv(file_path)
        logger.debug(f"Datafile head: {df.head()}")
        logger.debug(f"Datafile columns:\n {df.columns}")

        # Create an entry for a new data file in the database
        histogram_data_file, created = HistogramDataFile.objects.get_or_create(
            filepath=file_path,
            data_dimensionality=HistogramDataFile.DIMENSIONALITY_1D,
            data_era=data_era,
            granularity=HistogramDataFile.GRANULARITY_LUMISECTION)

        file_size = os.path.getsize(file_path)
        if not created and histogram_data_file.filesize != file_size:
            logger.warning(
                f"File '{file_path}' already in DB but size differs! "
                f"({histogram_data_file.filesize} bytes in DB, "
                f"{file_size} bytes actually)")

        # Update file size anyway
        histogram_data_file.filesize = file_size
        histogram_data_file.save()

        lumisection_histos1D = []  # New LumisectionHisto1D entries
        count = 0

        for index, row in df.iterrows():
            run_number = row["fromrun"]
            lumi_number = row["fromlumi"]
            title = row["hname"]
            entries = row["entries"]
            data = json.loads(row["histo"])

            logger.debug(
                f"Run: {run_number}\tLumisection: {lumi_number}\tTitle: {title}"
            )

            # Get existing or create new Run entry
            run, _ = Run.objects.get_or_create(run_number=run_number)

            # Get existing or create new Lumisection entry
            lumisection, _ = Lumisection.objects.get_or_create(
                run=run, ls_number=lumi_number)

            lumisection_histo1D = LumisectionHisto1D(
                lumisection=lumisection,
                title=title,
                entries=entries,
                data=data,
                source_data_file=histogram_data_file)

            lumisection_histos1D.append(lumisection_histo1D)
            count += 1

            # Bulk create every 50 entries
            if count == 50:

                LumisectionHisto1D.objects.bulk_create(lumisection_histos1D,
                                                       ignore_conflicts=True)
                logger.info(
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
