from os.path import getsize
from django.db import models

# from django.conf import settings


class HistogramDataFile(models.Model):
    """
    Model describing the generic characteristics of data files
    containing DQM histogram data (be they CSV or, in the future, nanoDQM files).

    - Each data file may contain either Run or Lumisection data and can be 1D or 2D.
    - Each file is parsed and stored into appropriate tables in the DB (e.g. 'LumisectionHisto1D')
    - Big (in the order of GB) files may be partially processed, so their current
    percentage_processed is stored for display purposes.
    """

    FILETYPE_UNKNOWN = "unk"
    FILETYPE_CSV = "csv"
    # FILETYPE_NANODQDM = 'nanodqm'  # TODO
    GRANULARITY_UNKNOWN = "unk"
    GRANULARITY_RUN = "run"
    GRANULARITY_LUMISECTION = "lum"
    DIMENSIONALITY_UNKNOWN = 0
    DIMENSIONALITY_1D = 1
    DIMENSIONALITY_2D = 2
    HISTOGRAM_DIMENSIONS_CHOICES = (
        (DIMENSIONALITY_UNKNOWN, "Unknown"),
        (DIMENSIONALITY_1D, "1D"),
        (DIMENSIONALITY_2D, "2D"),
    )
    DATAFILE_GRANULARITY_CHOICES = (
        (GRANULARITY_UNKNOWN, "Unknown"),
        (GRANULARITY_RUN, "Run"),
        (GRANULARITY_LUMISECTION, "Lumisection"),
    )

    DATAFILE_FORMAT_CHOICES = (
        # (FILETYPE_UNKNOWN, 'Unknown'), # Not needed
        (FILETYPE_CSV, "csv"),
        # (FILETYPE_NANODQDM, 'nanoDQM')
    )

    # DISABLED DUE TO PERFORMANCE ISSUES (see issue #30)
    # Recurse in Root filepath where all the DQM files are stored
    # filepath = models.FilePathField(path=settings.DIR_PATH_EOS_CMSML4DC,
    #                                 help_text="Path where the file is stored",
    #                                 recursive=True,
    #                                 max_length=255,
    #                                 match=".*\.csv",
    #                                 allow_folders=False)
    filepath = models.CharField(
        help_text="Path where the file is stored",
        max_length=255,
    )

    filesize = models.FloatField(default=0, help_text="The data file's size (Mbytes)")

    data_dimensionality = models.PositiveIntegerField(
        default=DIMENSIONALITY_UNKNOWN, choices=HISTOGRAM_DIMENSIONS_CHOICES, blank=True
    )

    data_era = models.CharField(
        blank=True,
        null=False,
        max_length=5,
        help_text="The era that the data refers to (e.g. 2018A)",
    )

    entries_total = models.PositiveIntegerField(
        default=0, help_text="Total number of entries contained in this histogram file"
    )

    entries_processed = models.PositiveIntegerField(
        default=0,
        help_text="Number of histogram entries that have been extracted from the file",
    )

    granularity = models.CharField(
        max_length=3,
        choices=DATAFILE_GRANULARITY_CHOICES,
        default=GRANULARITY_UNKNOWN,
        help_text="The granularity of the data contained in the "
        "data file (either whole run or lumisections)",
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def percentage_processed(self):
        return (
            ((self.entries_processed / self.entries_total) * 100)
            if self.entries_total > 0
            else 0
        )

    def save(self, *args, **kwargs):
        """
        Override save method to get file attributes on save
        """
        if self.filesize <= 0:
            self.filesize = getsize(self.filepath) / (1024 * 1024)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.filepath} ({self.filesize:.2f} MB)"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["filepath"], name="unique_filepath")
        ]
