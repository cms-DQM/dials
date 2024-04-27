from typing import ClassVar

from django.db import models


class Run(models.Model):
    """
    - Django doesn't support composite primary key
    - The unique constraint set in this class do not exist in the database,
    it is used here to select the composite primary key in the viewset and as a documentation
    """

    dataset_id = models.BigIntegerField(primary_key=True)
    run_number = models.IntegerField()
    ls_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "fact_run"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_fr_dataset_id", fields=["dataset_id"]),
            models.Index(name="idx_fr_run_number", fields=["run_number"]),
        ]
        constraints: ClassVar[list[models.Index]] = [
            models.UniqueConstraint(name="fact_run_primary_key", fields=["dataset_id", "run_number"]),
        ]

    def __str__(self) -> str:
        return f"Run <{self.run_number}@{self.dataset_id}>"
