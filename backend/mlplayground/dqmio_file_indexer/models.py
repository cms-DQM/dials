from pathlib import Path
from typing import List

from django.db import models
from django.core.exceptions import ValidationError


class FileIndexResponseBase:
    def __init__(self, storage: str, total: int, added: int, ingested_ids: List[int]):
        self.storage = storage
        self.total = total
        self.added = added
        self.ingested_ids = ingested_ids


class FileIndexStatus:
    INDEXED = "INDEXED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

    @staticmethod
    def all():
        return [
            key
            for key in FileIndexStatus.__dict__.keys()
            if key[:1] != "_" and key != "all"
        ]


class FileIndex(models.Model):
    VALID_FILE_EXTS = [".root"]
    is_cleaned = False

    file_path = models.CharField(
        help_text="Path where the file is stored", max_length=255
    )
    data_era = models.CharField(
        default="Unknown",
        null=False,
        max_length=7,
        help_text="The era that the data refers to (e.g. 2018A)",
    )
    n_entries = models.PositiveIntegerField(
        default=0, help_text="Total number of entries contained in this histogram file"
    )
    n_entries_ingested = models.PositiveIntegerField(
        default=0,
        help_text="Number of histogram entries that have been extracted from the file",
    )
    st_size = models.FloatField(default=0, help_text="The data file's size in bytes")
    st_ctime = models.DateTimeField(
        help_text="Time of files's last status change in filesystem"
    )
    st_itime = models.DateTimeField(
        auto_now_add=True, help_text="Time when file was indexed in database"
    )
    status = models.CharField(
        default=FileIndexStatus.INDEXED,
        null=False,
        max_length=max(len(v) for v in FileIndexStatus.all()),
        help_text="Indicate the processing status of run-histogram within the file",
    )

    def __str__(self):
        size_in_mb = self.st_size / 1024**2
        file_name = Path(self.file_path).name
        return f"{file_name} ({size_in_mb:.2f} MB)"

    def handle_filesize(self):
        if self.st_size <= 0:
            raise ValidationError("File is empty")

    def handle_status(self):
        if self.status not in FileIndexStatus.all():
            raise ValidationError("Invalid status")

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

    def update_status(self, value):
        if value not in FileIndexStatus.all():
            raise ValidationError("Invalid status entry")
        setattr(self, "status", value)
        self.save()

    def update_entries(self, field, value):
        if "entries" not in field:
            raise ValueError(
                "This function only update fields with 'entries' in their name"
            )
        setattr(self, field, value)
        self.save()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["file_path"], name="unique_file_path")
        ]
