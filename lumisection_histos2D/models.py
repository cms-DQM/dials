import os.path
import logging
import json

# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
import pandas as pd
from django.db import models
from runs.models import Run
from lumisections.models import Lumisection
from django.contrib.postgres.fields import ArrayField
from histogram_file_manager.models import HistogramDataFile

logger = logging.getLogger(__name__)

LUMISECTION_HISTOGRAM_2D_CHUNK_SIZE = 50


class LumisectionHisto2D(models.Model):
    """
    Model containing 2D Lumisection Histogram information
    """

    lumisection = models.ForeignKey(Lumisection, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=100)
    data = ArrayField(models.FloatField(), blank=True)
    # ArrayField( ArrayField( models.IntegerField(blank=True), size=XX, ), size=XX,)
    entries = models.IntegerField(blank=True, null=True)
    x_min = models.FloatField(blank=True, null=True)
    x_max = models.FloatField(blank=True, null=True)
    x_bin = models.IntegerField(blank=True, null=True)
    y_max = models.FloatField(blank=True, null=True)
    y_min = models.FloatField(blank=True, null=True)
    y_bin = models.IntegerField(blank=True, null=True)
    source_data_file = models.ForeignKey(
        HistogramDataFile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=
        "Source data file that the specific Histogram was read from, if any",
    )

    @staticmethod
    def from_csv(file_path, data_era: str = ""):
        """
        Import 2D Lumisection Histograms from a csv file
        """
        logger.info(
            f"Importing 2D Lumisection Histograms from '{file_path}', "
            f"splitting into chunks of {LUMISECTION_HISTOGRAM_2D_CHUNK_SIZE}")

        # Create an entry for a new data file in the database
        histogram_data_file, created = HistogramDataFile.objects.get_or_create(
            filepath=file_path,
            data_dimensionality=HistogramDataFile.DIMENSIONALITY_2D,
            data_era=data_era,
            granularity=HistogramDataFile.GRANULARITY_LUMISECTION,
        )

        file_size = os.path.getsize(file_path)

        # Get number of lines, this may take a "long" time, but
        # it's needed to record our progress while parsing the file
        with open(file_path, 'r') as fp:
            for file_line_count, line in enumerate(fp):
                pass

        # Histogram file was already recorded in database
        if not created and histogram_data_file.filesize != file_size:
            logger.warning(
                f"File '{file_path}' already in DB but size differs! "
                f"({histogram_data_file.filesize} bytes in DB, "
                f"{file_size} bytes actually)")

        # Update file size anyway
        histogram_data_file.filesize = file_size
        histogram_data_file.save()

        # Keep track of current chunk
        current_chunk = 0
        # Keep track of lines read
        num_lines_read = 0
        reader = pd.read_csv(file_path,
                             chunksize=LUMISECTION_HISTOGRAM_2D_CHUNK_SIZE)
        logger.info(f"File has {file_line_count} lines")
        for df in reader:
            logger.debug(f"Reading chunk {current_chunk}")
            lumisection_histos2D = []

            for index, row in df.iterrows():
                run_number = row["fromrun"]
                lumi_number = row["fromlumi"]
                title = row["hname"]
                entries = row["entries"]
                data = json.loads(row["histo"])
                logger.debug(
                    f"Run: {run_number}\tLumisection: {lumi_number}\tTitle: {title}"
                )

                run, _ = Run.objects.get_or_create(run_number=run_number)
                lumisection, _ = Lumisection.objects.get_or_create(
                    run=run, ls_number=lumi_number)

                lumisection_histo2D = LumisectionHisto2D(
                    lumisection=lumisection,
                    title=title,
                    entries=entries,
                    data=data,
                    source_data_file=histogram_data_file)
                lumisection_histos2D.append(lumisection_histo2D)

            LumisectionHisto2D.objects.bulk_create(lumisection_histos2D,
                                                   ignore_conflicts=True)

            logger.info(
                f"{len(lumisection_histos2D)} x "
                f"2D lumisection histos successfully added from chunk {current_chunk}!"
            )
            num_lines_read += len(lumisection_histos2D)
            current_chunk += 1
            # Record progress in DB
            # Not safe to assume progress by chunks read,
            # the last chunk may have less lines than expected
            histogram_data_file.percentage_processed = (num_lines_read /
                                                        file_line_count) * 100
            histogram_data_file.save()  # Save entries and move to next chunk

    def __str__(self):
        return f"run {self.lumisection.run.run_number} / lumisection {self.lumisection.ls_number} / name {self.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["lumisection", "title"],
                name="unique run / ls / 2d histogram combination",
            )
        ]
