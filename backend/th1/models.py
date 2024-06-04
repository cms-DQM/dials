from typing import ClassVar

from django.contrib.postgres.fields import ArrayField
from django.db import models


class TH1(models.Model):
    """
    - Django doesn't support composite primary key
    - The unique constraint set in this class do not exist in the database,
    it is used here to select the composite primary key in the viewset and as a documentation
    """

    dataset_id = models.BigIntegerField(primary_key=True)
    file_id = models.BigIntegerField()
    run_number = models.IntegerField()
    ls_number = models.IntegerField()
    me_id = models.IntegerField()
    x_min = models.FloatField()
    x_max = models.FloatField()
    x_bin = models.IntegerField()
    entries = models.IntegerField()
    data = ArrayField(models.FloatField())

    class Meta:
        managed = False
        db_table = "fact_th1"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_th1_file_id", fields=["file_id"]),
            models.Index(name="idx_th1_run_number", fields=["run_number"]),
            models.Index(name="idx_th1_ls_number", fields=["ls_number"]),
            models.Index(name="idx_th1_me_id", fields=["me_id"]),
            models.Index(name="idx_th1_run_number_me_id", fields=["run_number", "me_id"]),
        ]
        constraints: ClassVar[list[models.Index]] = [
            models.UniqueConstraint(
                name="fact_th1_primary_key", fields=["dataset_id", "run_number", "ls_number", "me_id"]
            ),
        ]

    def __str__(self) -> str:
        return f"TH1 <{self.file_id}>"
