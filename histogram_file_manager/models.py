from django.db import models
from django.conf import settings


class HistogramDataFile(models.Model):
    """
    Model describing the generic characteristics of data files 
    containing DQM histogram data (be they CSV or, in the future, nanoDQM files).

    - Each data file may contain either Run or Lumisection data and can be 1D or 2D.
    - Each file is parsed and stored into appropriate tables in the DB (e.g. 'LumisectionHisto1D')
    - Big (in the order of GB) files may be partially processed, so their current
    percentage_processed is stored for display purposes.
    """
    RUN = 'run'
    LUMISECTION = 'lum'
    HISTOGRAM_DIMENSIONS_CHOICES = ((1, '1D'), (2, '2D'))
    DATAFILE_GRANULARITY_CHOICES = ((RUN, 'Run'), (LUMISECTION, 'Lumisection'))

    # Recurse in Root filepath where all the DQM files are stored
    filepath = models.FilePathField(path=settings.FILE_PATH_EOS_CMSML4DC,
                                    help_text="Path where the file is stored",
                                    recursive=True)

    filesize = models.PositiveIntegerField(
        default=0, blank=True, help_text="The data file's size (bytes)")

    data_era = models.CharField(
        blank=False,
        null=False,
        max_length=5,
        help_text="The era that the data refers to (e.g. 2018A)")

    percentage_processed = models.FloatField(
        default=0.0,
        help_text=
        "Percentage of file which has been processed and added to the DB")

    granularity = models.CharField(
        max_length=3,
        choices=DATAFILE_GRANULARITY_CHOICES,
        default=RUN,
        help_text="The granularity of the data contained in the "\
        "data file (either whole run or lumisections)")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['filepath'],
                                    name="unique_filepath")
        ]
