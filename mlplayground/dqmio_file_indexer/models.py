from pathlib import Path

from django.db import models
from django.core.exceptions import ValidationError


class FileIndexResponseBase:
    def __init__(self, storage, total, added):
        self.storage = storage
        self.total = total
        self.added = added


class FileIndex(models.Model):
    VALID_FILE_EXTS = [".root"]
    VALID_FILE_STATUS = {"indexed": "INDEXED", "pending": "PENDING", "running": "RUNNING", "ok": "OK", "failed": "FAILED"}
    is_cleaned = False

    file_path = models.CharField(
        help_text="Path where the file is stored",
        max_length=255
    )
    data_era = models.CharField(
        default="Unknown",
        null=False,
        max_length=7,
        help_text="The era that the data refers to (e.g. 2018A)",
    )
    n_entries = models.PositiveIntegerField(
        default=0,
        help_text="Total number of entries contained in this histogram file"
    )
    n_entries_ingested = models.PositiveIntegerField(
        default=0,
        help_text="Number of histogram entries that have been extracted from the file",
    )
    st_size = models.FloatField(
        default=0,
        help_text="The data file's size in bytes"
    )
    st_ctime = models.DateTimeField(
        help_text="Time of files's last status change in filesystem"
    )
    st_mtime = models.DateTimeField(
        help_text="Time of files's last modification in filesystem"
    )
    st_itime = models.DateTimeField(
        auto_now_add=True,
        help_text="Time when file was indexed in database"
    )
    st_imtime = models.DateTimeField(
        auto_now=True,
        help_text="Time when index entry was modified in database"
    )
    status_rh = models.CharField(
        default=VALID_FILE_STATUS.get("indexed"),
        null=False,
        max_length=30,
        help_text="Indicate the processing status of run-histogram within the file"
    )
    status_h1d = models.CharField(
        default=VALID_FILE_STATUS.get("indexed"),
        null=False,
        max_length=30,
        help_text="Indicate the processing status of 1d-histograms within the file"
    )
    status_h2d = models.CharField(
        default=VALID_FILE_STATUS.get("indexed"),
        null=False,
        max_length=30,
        help_text="Indicate the processing status of 2d-histograms within the file"
    )

    def __str__(self):
        size_in_mb = self.st_size/1024**2
        file_name = Path(self.file_path).name
        return f"{file_name} ({size_in_mb:.2f} MB)"
    
    def handle_filesize(self):
        if self.st_size <= 0:
            raise ValidationError("File is empty")
    
    def handle_status(self):
        if self.status_rh not in self.VALID_FILE_STATUS.values():
            raise ValidationError("Invalid status for status_rh")
        if self.status_h1d not in self.VALID_FILE_STATUS.values():
            raise ValidationError("Invalid status for status_h1d")
        if self.status_h2d not in self.VALID_FILE_STATUS.values():
            raise ValidationError("Invalid status for status_h2d")

    def handle_file_ext(self):
        if Path(self.file_path).suffix not in self.VALID_FILE_EXTS:
            raise ValidationError("Invalid file extension")

    def clean(self):
        self.handle_filesize()
        self.handle_status()
        self.handle_file_ext()

    def save(self, *args, **kwargs):
        """
        Override save method to get file attributes on save
        """
        if not self.is_cleaned:
            try:
                self.full_clean()
            except ValidationError as err:
                print(err)
                raise err

        super().save(*args, **kwargs)

    def update_status(self, field, key):
        value = self.VALID_FILE_STATUS.get(key)
        if value is None:
            raise ValidationError("Invalid entry status")
        if "status" not in field:
            raise ValueError("This function only update fields with 'status' in their name")
        setattr(self, field, value)
        self.save()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["file_path"], name="unique_file_path")
        ]
