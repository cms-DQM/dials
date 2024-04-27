from typing import ClassVar

from django.db import models


class MEs(models.Model):
    me_id = models.AutoField(primary_key=True)
    me = models.CharField()
    count = models.IntegerField()
    dim = models.IntegerField()

    class Meta:
        managed = False
        db_table = "dim_monitoring_elements"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_me", fields=["me"]),
        ]
        constraints: ClassVar[list[models.Index]] = [
            models.UniqueConstraint(name="unique_me", fields=["me"]),
        ]

    def __str__(self) -> str:
        return f"ME <{self.me_id}>"
