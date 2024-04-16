from typing import ClassVar

from django.contrib.postgres.fields import ArrayField
from django.db import models
from dqmio_file_indexer.models import FileIndex


class Run(models.Model):
    run_number = models.IntegerField(primary_key=True)
    ls_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "run"

    def __str__(self) -> str:
        return f"Run <{self.run_number}>"


class Lumisection(models.Model):
    ls_id = models.BigIntegerField(primary_key=True)
    ls_number = models.IntegerField()
    th1_count = models.IntegerField()
    th2_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "lumisection"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_ls_number", fields=["ls_number"]),
        ]

    def __str__(self) -> str:
        return f"Lumisection <{self.ls_number}@{self.ls_id}>"


class LumisectionHistogram1DMEs(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    count = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "th1_mes"

    def __str__(self) -> str:
        return f"LumisectionHistogram1DMEs <{self.title}>"


class LumisectionHistogram1D(models.Model):
    hist_id = models.BigIntegerField(primary_key=True)
    file_id = models.ForeignKey(FileIndex, on_delete=models.CASCADE, db_column="file_id")
    run_number = models.ForeignKey(Run, on_delete=models.CASCADE, db_column="run_number")
    ls_id = models.ForeignKey(Lumisection, on_delete=models.CASCADE, db_column="ls_id")
    title = models.CharField(max_length=255)
    x_min = models.FloatField()
    x_max = models.FloatField()
    x_bin = models.IntegerField()
    entries = models.IntegerField()
    data = ArrayField(models.FloatField())

    class Meta:
        managed = False
        db_table = "th1"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_th1_file_id", fields=["file_id"]),
            models.Index(name="idx_th1_run_number", fields=["run_number"]),
            models.Index(name="idx_th1_ls_id", fields=["ls_id"]),
            models.Index(name="idx_th1_title", fields=["title"]),
            models.Index(name="idx_th1_entries", fields=["entries"]),
        ]

    def __str__(self) -> str:
        return f"LumisectionHistogram1D <{self.hist_id}>"


class LumisectionHistogram2DMEs(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    count = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "th2_mes"

    def __str__(self) -> str:
        return f"LumisectionHistogram2DMEs <{self.title}>"


class LumisectionHistogram2D(models.Model):
    hist_id = models.BigIntegerField(primary_key=True)
    file_id = models.ForeignKey(FileIndex, on_delete=models.CASCADE, db_column="file_id")
    run_number = models.ForeignKey(Run, on_delete=models.CASCADE, db_column="run_number")
    ls_id = models.ForeignKey(Lumisection, on_delete=models.CASCADE, db_column="ls_id")
    title = models.CharField(max_length=255)
    x_min = models.FloatField()
    x_max = models.FloatField()
    x_bin = models.IntegerField()
    y_min = models.FloatField()
    y_max = models.FloatField()
    y_bin = models.IntegerField()
    entries = models.IntegerField()
    data = ArrayField(ArrayField(models.FloatField()))

    class Meta:
        managed = False
        db_table = "th2"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(name="idx_th2_file_id", fields=["file_id"]),
            models.Index(name="idx_th2_run_number", fields=["run_number"]),
            models.Index(name="idx_th2_ls_id", fields=["ls_id"]),
            models.Index(name="idx_th2_title", fields=["title"]),
            models.Index(name="idx_th2_entries", fields=["entries"]),
        ]

    def __str__(self) -> str:
        return f"LumisectionHistogram2D <{self.hist_id}>"
