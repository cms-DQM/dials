from typing import ClassVar

from django.db import models


class MLModelsIndex(models.Model):
    model_id = models.IntegerField(primary_key=True)
    filename = models.CharField(max_length=255)
    target_me = models.CharField(max_length=255)
    thr = models.FloatField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "dim_ml_models_index"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_active", fields=["active"]),
        ]

    def __str__(self) -> str:
        return f"Model <{self.model_id}>"
