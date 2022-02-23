from django.db import models

# Create your models here.
class Dataset(models.Model):
    STORAGE_CHOICES = (
        ("postgres", "Postgres"),
        ("eos", "EOS"),
        ("external", "External")
    )

    GRANULAR_CHOICES = (
        ("fill", "Fill"),
        ("run", "Run"),
        ("lumi", "Lumisection")
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    storagetype = models.CharField(choices=STORAGE_CHOICES, max_length=50)
    granularity = models.CharField(choices=GRANULAR_CHOICES, max_length=50)
    api = models.TextField(blank = True)
    api_description = models.TextField(blank = True)
    location = models.TextField(blank = True)
    scripts = models.TextField(blank = True)
    comment = models.TextField(blank = True)
    data_view = models.TextField(blank = True)
    
    def __str__(self):
        return "{}".format(self.name)
