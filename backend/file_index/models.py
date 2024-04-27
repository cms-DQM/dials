from typing import ClassVar

from django.db import models


class FileIndex(models.Model):
    dataset_id = models.BigIntegerField()
    file_id = models.BigIntegerField(primary_key=True)
    file_size = models.BigIntegerField()
    creation_date = models.DateTimeField()
    last_modification_date = models.DateTimeField()
    logical_file_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    err_trace = models.CharField(max_length=2295, default="")

    class Meta:
        managed = False
        db_table = "fact_file_index"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_fdi_dataset_id", fields=["dataset_id"]),
            models.Index(name="idx_fdi_logical_file_name", fields=["logical_file_name"]),
            models.Index(name="idx_fdi_status", fields=["status"]),
        ]

    def __str__(self) -> str:
        return f"FileIndex <{self.file_id}>"
