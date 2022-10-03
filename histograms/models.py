import time
import os.path
import json
import logging
import pandas as pd  # https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
import numpy as np

from django.db import models
from django.contrib.postgres.fields import ArrayField

from data_taking_objects.models import Run, Lumisection
from histogram_file_manager.models import HistogramDataFile

logger = logging.getLogger(__name__)

# Specifies the number of lines that the csv file will be
# chunked into during parsing 2D histograms.
# E.g. 50 means that a 120-line csv will be read in two 50-line chunks
# and one 20-line chunk.
LUMISECTION_HISTOGRAM_2D_CHUNK_SIZE = 50


class HistogramBase(models.Model):
    """
    Base model to be inherited from Run and Lumisection Histograms
    """

    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=220)
    source_data_file = models.ForeignKey(
        HistogramDataFile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Source data file that the specific Histogram was read from, if any",
        related_name="%(class)s",
    )

    class Meta:
        abstract = True


class RunHistogram(HistogramBase):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="histograms")
    primary_dataset = models.CharField(max_length=220)
    path = models.CharField(max_length=220)
    entries = models.BigIntegerField(null=True)
    mean = models.FloatField(null=True)
    rms = models.FloatField(null=True)
    skewness = models.FloatField(null=True)
    kurtosis = models.FloatField(null=True)

    def __str__(self):
        return f"run: {self.run.run_number} / dataset: {self.primary_dataset} / histo: {self.title}"

    # TODO
    class Meta:
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                fields=["run", "primary_dataset", "title"],
                name="unique run/dataset/histogram combination",
            )
        ]


class LumisectionHistogramBase(HistogramBase):
    """
    Abstract Base model that both 1D and 2D lumisection histograms inherit from.

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

    data = ArrayField(models.FloatField(), blank=True)
    x_min = models.FloatField(blank=True, null=True)
    x_max = models.FloatField(blank=True, null=True)
    x_bin = models.IntegerField(blank=True, null=True)

    @staticmethod
    def from_csv(file_path, data_era: str = ""):
        """
        Import 1D Lumisection Histograms from a csv file
        """
        df = pd.read_csv(file_path)
        logger.debug(f"Datafile head: {df.head()}")
        # logger.debug(f"Datafile columns:\n {df.columns}")

        # Create an entry for a new data file in the database
        histogram_data_file, created = HistogramDataFile.objects.get_or_create(
            filepath=file_path
        )
        histogram_data_file.data_dimensionality = HistogramDataFile.DIMENSIONALITY_1D
        histogram_data_file.data_era = data_era
        histogram_data_file.granularity = HistogramDataFile.GRANULARITY_LUMISECTION

        # file_size = os.path.getsize(file_path)
        file_line_count = 0  # Total lines in CSV

        # Get number of lines, this may take a "long" time, but
        # it's needed to record our progress while parsing the file
        if histogram_data_file.entries_total < 1:
            logger.debug(f"Counting total lines for file {file_path}")
            with open(file_path, "r") as fp:
                for file_line_count, line in enumerate(fp):
                    pass
            logger.debug(f"File {file_path} has {file_line_count} lines")

            histogram_data_file.entries_total = file_line_count
            histogram_data_file.save()

        lumisection_histos1D = []  # New LumisectionHisto1D entries
        count = 0

        for index, row in df.iterrows():
            run_number = row["fromrun"]
            lumi_number = row["fromlumi"]
            title = row["hname"]
            entries = row["entries"]
            data = json.loads(row["histo"])
            hist_x_min  = row["Xmin"]
            hist_x_max  = row["Xmax"]
            hist_x_bins = row["Xbins"]

            data = data[1:hist_x_bins+1]

            #logger.debug(
            #    f"Run: {run_number}\tLumisection: {lumi_number}\tTitle: {title}\tlength: {len(data)}"
            #)

            # Get existing or create new Run entry
            run, _ = Run.objects.get_or_create(run_number=run_number)

            # Get existing or create new Lumisection entry
            lumisection, _ = Lumisection.objects.get_or_create(
                run=run, ls_number=lumi_number
            )

            lumisection_histo1D = LumisectionHistogram1D(
                lumisection=lumisection,
                title=title,
                entries=entries,
                data=data,
                source_data_file=histogram_data_file,
                x_min = hist_x_min,
                x_max = hist_x_max,
                x_bin = hist_x_bins,
            )

            lumisection_histos1D.append(lumisection_histo1D)
            count += 1

            # Bulk create every 50 entries
            if count == 50:

                LumisectionHistogram1D.objects.bulk_create(
                    lumisection_histos1D, ignore_conflicts=True
                )
                logger.info("50 lumisections 1D histograms successfully added!")
                histogram_data_file.entries_processed += 50
                histogram_data_file.save()
                count = 0
                lumisection_histos1D = []

            time.sleep(0.1)  # Don't be greedy!

        if (
            lumisection_histos1D
        ):  # If total entries not a multiple of 50, some will be left
            LumisectionHistogram1D.objects.bulk_create(
                lumisection_histos1D, ignore_conflicts=True
            )
            histogram_data_file.entries_processed += len(lumisection_histos1D)
            histogram_data_file.save()

    def __str__(self):
        return f"run {self.lumisection.run.run_number} / lumisection {self.lumisection.ls_number} / name {self.title}"

    # TODO
    class Meta:
        verbose_name_plural = "Lumisection Histograms 1D"
        constraints = [
            models.UniqueConstraint(
                fields=["lumisection", "title"],
                name="unique run / ls / 1d histogram combination",
            )
        ]


def get_last_chunk(histogram_data_file, chunk_size):
    """
    Function that calculates the last chunk that was parsed from
    a 2D Lumisection histogram csv file.
    """
    return int(histogram_data_file.entries_processed / chunk_size)


class LumisectionHistogram2D(LumisectionHistogramBase):
    """
    Model containing 2D Lumisection Histogram information
    """

    data = ArrayField(
        ArrayField(
            models.FloatField(),
            blank=True
        ),
        blank=True
    )
    #data_numpy = ArrayField(models.BinaryField())
    # ArrayField( ArrayField( models.IntegerField(blank=True), size=XX, ), size=XX,)
    x_min = models.FloatField(blank=True, null=True)
    x_max = models.FloatField(blank=True, null=True)
    x_bin = models.IntegerField(blank=True, null=True)
    y_max = models.FloatField(blank=True, null=True)
    y_min = models.FloatField(blank=True, null=True)
    y_bin = models.IntegerField(blank=True, null=True)

    @staticmethod
    def from_csv(
        file_path, data_era: str = "", resume: bool = True, read_chunk_num_max: int = -1
    ):
        """
        Import 2D Lumisection Histograms from a csv file

        Parameters:
        - file_path: A path to a .csv file containing a 2D Lumisection Histogram
        - data_era: The era that the data refers to (e.g. 2018A)
        - resume: Specify whether the function will continue parsing from the last
        parsed chunk
        """
        logger.info(
            f"Importing 2D Lumisection Histograms from '{file_path}', "
            f"splitting into chunks of {LUMISECTION_HISTOGRAM_2D_CHUNK_SIZE}"
        )

        # Create an entry for a new data file in the database
        histogram_data_file, created = HistogramDataFile.objects.get_or_create(
            filepath=file_path
        )
        histogram_data_file.data_dimensionality = HistogramDataFile.DIMENSIONALITY_2D
        histogram_data_file.data_era = data_era
        histogram_data_file.granularity = HistogramDataFile.GRANULARITY_LUMISECTION

        # file_size = os.path.getsize(file_path)
        file_line_count = 0  # Total lines in CSV

        # Get number of lines, this may take a "long" time, but
        # it's needed to record our progress while parsing the file
        if histogram_data_file.entries_total < 1:
            logger.debug(f"Counting total lines for file {file_path}")
            with open(file_path, "r") as fp:
                for file_line_count, line in enumerate(fp):
                    pass
            logger.debug(f"File {file_path} has {file_line_count} lines")
            histogram_data_file.entries_total = file_line_count
            histogram_data_file.save()

        # Last saved chunk in DB.
        last_chunk = (
            0
            if created
            else get_last_chunk(
                histogram_data_file, LUMISECTION_HISTOGRAM_2D_CHUNK_SIZE
            )
            if resume
            else 0
        )

        logger.info(f"Last chunk: {last_chunk}")
        # Keep track of current chunk
        current_chunk = 0
        # Keep track of lines read
        num_lines_read = 0
        reader = pd.read_csv(file_path, chunksize=LUMISECTION_HISTOGRAM_2D_CHUNK_SIZE)
        for df in reader:
            if resume and current_chunk < last_chunk:
                logger.debug(f"Skipping chunk {current_chunk}")
                current_chunk += 1
                num_lines_read += LUMISECTION_HISTOGRAM_2D_CHUNK_SIZE
                continue
            else:
                logger.debug(f"Reading chunk {current_chunk}")
            lumisection_histos2D = []

            for index, row in df.iterrows():
                run_number = row["fromrun"]
                lumi_number = row["fromlumi"]
                title = row["hname"]
                entries = row["entries"]
                data = json.loads(row["histo"])
                hist_x_min = float(row["Xmin"])
                hist_x_max = float(row["Xmax"])
                hist_x_bins = int(row["Xbins"])
                hist_y_min = float(row["Ymin"])
                hist_y_max = float(row["Ymax"])
                hist_y_bins = int(row["Ybins"])

                data = np.reshape(np.asarray(data), (hist_y_bins+2, hist_x_bins+2))
                data = data[1:hist_y_bins+1, 1:hist_x_bins+1]
                data = data.tolist()

                #logger.debug(
                #    f"Run: {run_number}\tLumisection: {lumi_number}\tTitle: {title}\txbins: {hist_x_bins}\tybins: {hist_y_bins}\tshape: {np.asarray(data).shape}"
                #)

                run, _ = Run.objects.get_or_create(run_number=run_number)
                lumisection, _ = Lumisection.objects.get_or_create(
                    run=run, ls_number=lumi_number
                )

                lumisection_histo2D = LumisectionHistogram2D(
                    lumisection=lumisection,
                    title=title,
                    entries=entries,
                    data=data,
                    source_data_file=histogram_data_file,
                    x_min = hist_x_min,
                    x_max = hist_x_max,
                    x_bin = hist_x_bins,
                    y_min = hist_y_min,
                    y_max = hist_y_max,
                    y_bin = hist_y_bins,
                )
                lumisection_histos2D.append(lumisection_histo2D)

                #time.sleep(0.1)  # Don't be greedy!

            LumisectionHistogram2D.objects.bulk_create(
                lumisection_histos2D, ignore_conflicts=True
            )

            logger.info(
                f"{len(lumisection_histos2D)} x "
                f"2D lumisection histos successfully added from chunk {current_chunk}!"
            )
            num_lines_read += len(lumisection_histos2D)
            current_chunk += 1
            # Record progress in DB
            # Not safe to assume progress by chunks read,
            # the last chunk may have less lines than expected
            histogram_data_file.entries_processed = num_lines_read
            histogram_data_file.save()  # Save entries and move to next chunk

            # User can decide up to which chunk to read
            if read_chunk_num_max >= current_chunk:
                logger.info(
                    f"Read until requested chunk {read_chunk_num_max}, stopping"
                )
                break

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
