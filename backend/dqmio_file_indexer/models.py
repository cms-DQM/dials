from pathlib import Path
from typing import ClassVar

from django.core.exceptions import ValidationError
from django.db import models


class FileIndexStatus:
    INDEXED = "INDEXED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

    @staticmethod
    def all():
        return [key for key in FileIndexStatus.__dict__.keys() if key[:1] != "_" and key != "all"]


class FileIndex(models.Model):
    VALID_FILE_EXTS: ClassVar[list[str]] = [".root"]
    is_cleaned = False

    file_uuid = models.CharField(help_text="ROOT TFile UUID", max_length=36)
    file_path = models.CharField(help_text="Path where the file is stored", max_length=255)
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
    st_ctime = models.DateTimeField(help_text="Time of files's last status change in filesystem")
    st_itime = models.DateTimeField(auto_now_add=True, help_text="Time when file was indexed in database")
    status = models.CharField(
        default=FileIndexStatus.INDEXED,
        null=False,
        max_length=max(len(v) for v in FileIndexStatus.all()),
        help_text="Indicate the processing status of run-histogram within the file",
    )

    class Meta:
        constraints: ClassVar[list[models.UniqueConstraint]] = [
            models.UniqueConstraint(fields=["file_uuid"], name="unique_file_uuid")
        ]
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["file_path"]),
            models.Index(fields=["data_era"]),
            models.Index(fields=["st_size"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        size_in_mb = self.st_size / 1024**2
        file_name = Path(self.file_path).name
        return f"{file_name} ({size_in_mb:.2f} MB)"

    def save(self, *args, **kwargs):
        """
        Override save method to get file attributes on save
        """
        if not self.is_cleaned:
            try:
                self.full_clean()
            except ValidationError as err:
                raise err

        super().save(*args, **kwargs)

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

    def update_status(self, value):
        if value not in FileIndexStatus.all():
            raise ValidationError("Invalid status entry")
        self.status = value
        self.save()

    def update_entries(self, field, value):
        if "entries" not in field:
            raise ValueError("This function only update fields with 'entries' in their name")
        setattr(self, field, value)
        self.save()


class BadFileIndex(models.Model):
    file_path = models.CharField(help_text="Path where the file is stored", max_length=255)
    data_era = models.CharField(
        default="Unknown",
        null=False,
        max_length=7,
        help_text="The era that the data refers to (e.g. 2018A)",
    )
    st_size = models.FloatField(default=0, help_text="The data file's size in bytes")
    st_ctime = models.DateTimeField(help_text="Time of files's last status change in filesystem")
    st_itime = models.DateTimeField(auto_now_add=True, help_text="Time when file was indexed in database")
    err = models.CharField(max_length=255, help_text="Error message")

    # TODO
    # Instead of putting an UniqueConstraint in file_path (if path changes, new files will be added)
    # check if it is possible to put the constraint in the file_name without creating a new field
    class Meta:
        constraints: ClassVar[list[models.UniqueConstraint]] = [
            models.UniqueConstraint(fields=["file_path"], name="unique_bad_file_path")
        ]

    def __str__(self):
        size_in_mb = self.st_size / 1024**2
        file_name = Path(self.file_path).name
        return f"BAD {file_name} ({size_in_mb:.2f} MB)"
