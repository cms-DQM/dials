from django.db import models


# Create your models here.
class Run(models.Model):
    run_number = models.IntegerField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"run {self.run_number}"
