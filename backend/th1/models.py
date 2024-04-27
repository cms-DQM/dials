from typing import ClassVar

from django.contrib.postgres.fields import ArrayField
from django.db import models


class TH1(models.Model):
    hist_id = models.BigIntegerField(primary_key=True)
    dataset_id = models.BigIntegerField()
    file_id = models.BigIntegerField()
    run_number = models.IntegerField()
    ls_number = models.IntegerField()
    me_id = models.IntegerField()
    ls_id = models.BigIntegerField()
    x_min = models.FloatField()
    x_max = models.FloatField()
    x_bin = models.IntegerField()
    entries = models.IntegerField()
    data = ArrayField(models.FloatField())

    class Meta:
        managed = False
        db_table = "fact_th1"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_th1_dataset_id", fields=["dataset_id"]),
            models.Index(name="idx_th1_file_id", fields=["file_id"]),
            models.Index(name="idx_th1_run_number", fields=["run_number"]),
            models.Index(name="idx_th1_ls_number", fields=["ls_number"]),
            models.Index(name="idx_th1_me_id", fields=["me_id"]),
            models.Index(name="idx_th1_ls_id", fields=["ls_id"]),
        ]

    def __str__(self) -> str:
        return f"TH1 <{self.file_id}>"
