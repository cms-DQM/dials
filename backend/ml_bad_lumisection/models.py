from typing import ClassVar

from django.db import models


class MLBadLumisection(models.Model):
    """
    - Django doesn't support composite primary key
    - The unique constraint set in this class do not exist in the database,
    it is used here to select the composite primary key in the viewset and as a documentation
    """

    model_id = models.BigIntegerField(primary_key=True)
    dataset_id = models.BigIntegerField()
    file_id = models.BigIntegerField()
    run_number = models.IntegerField()
    ls_number = models.IntegerField()
    me_id = models.IntegerField()
    mse = models.FloatField()

    class Meta:
        managed = False
        db_table = "fact_ml_bad_lumis"
        constraints: ClassVar[list[models.Index]] = [
            models.UniqueConstraint(
                name="fact_ml_bad_lumis_primary_key",
                fields=["model_id", "dataset_id", "run_number", "ls_number", "me_id"],
            ),
        ]

    def __str__(self) -> str:
        return f"MLBadLumisection <{self.me_id}@{self.ls_number}@{self.run_number}@{self.dataset_id}@{self.model_id}>"
