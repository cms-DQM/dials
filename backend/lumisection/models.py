from typing import ClassVar

from django.db import models


class Lumisection(models.Model):
    """
    - Django doesn't support composite primary key
    - The unique constraint set in this class do not exist in the database,
    it is used here to select the composite primary key in the viewset and as a documentation
    """

    dataset_id = models.BigIntegerField(primary_key=True)
    run_number = models.IntegerField()
    ls_number = models.IntegerField()
    ls_id = models.BigIntegerField()
    th1_count = models.IntegerField()
    th2_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "fact_lumisection"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_fls_ls_id", fields=["ls_id"]),
            models.Index(name="idx_fls_dataset_id", fields=["dataset_id"]),
            models.Index(name="idx_fls_run_number", fields=["run_number"]),
            models.Index(name="idx_fls_ls_number", fields=["ls_number"]),
        ]
        constraints: ClassVar[list[models.Index]] = [
            models.UniqueConstraint(
                name="fact_lumisection_primary_key", fields=["dataset_id", "run_number", "ls_number"]
            ),
        ]

    def __str__(self) -> str:
        return f"Lumisection <{self.ls_number}@{self.run_number}@{self.dataset_id}>"
