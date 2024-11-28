from typing import ClassVar

from django.db import models


class DatasetIndex(models.Model):
    dataset_id = models.BigIntegerField(primary_key=True)
    dataset = models.CharField(max_length=255)
    era = models.CharField(max_length=255)
    data_tier = models.CharField(max_length=255)
    primary_ds_name = models.CharField(max_length=255)
    processed_ds_name = models.CharField(max_length=255)
    processing_version = models.IntegerField()
    last_modification_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "fact_dataset_index"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_dataset", fields=["dataset"]),
            models.Index(name="idx_era", fields=["era"]),
        ]

    def __str__(self) -> str:
        return f"DatasetIndex <{self.dataset_id}>"
