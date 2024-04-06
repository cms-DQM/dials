from typing import ClassVar

from django.db import models


class FileIndex(models.Model):
    file_id = models.BigIntegerField(primary_key=True)
    file_size = models.BigIntegerField()
    era = models.CharField(max_length=5)
    campaign = models.CharField(max_length=15)
    dataset = models.CharField(max_length=50)
    creation_date = models.DateTimeField()
    last_modification_date = models.DateTimeField()
    logical_file_name = models.CharField(max_length=255)
    status = models.CharField(max_length=15)
    err_trace = models.CharField(max_length=5000, default="")

    class Meta:
        managed = False
        db_table = "dqmio_index"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_file_size", fields=["file_size"]),
            models.Index(name="idx_era", fields=["era"]),
            models.Index(name="idx_campaign", fields=["campaign"]),
            models.Index(name="idx_dataset", fields=["dataset"]),
            models.Index(name="idx_logical_file_name", fields=["logical_file_name"]),
            models.Index(name="idx_status", fields=["status"]),
        ]

    def __str__(self) -> str:
        return f"FileIndex <{self.file_id}>"
