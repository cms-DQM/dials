from django.db import models

# Create your models here.
class Run(models.Model):
    run_number = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"run {run_number}"
