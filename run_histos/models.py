from django.db import models
from runs.models import Run


# Create your models here.
class RunHisto(models.Model):
    run             = models.ForeignKey(Run, on_delete=models.CASCADE)
    date            = models.DateTimeField(auto_now_add=True)

    primary_dataset = models.CharField(max_length=220)
    path            = models.CharField(max_length=220)
    title           = models.CharField(max_length=220)

    entries         = models.IntegerField(null=True)
    mean            = models.FloatField(null=True)
    rms             = models.FloatField(null=True)
    skewness        = models.FloatField(null=True)
    kurtosis        = models.FloatField(null=True)

    def __str__(self):
        return f"run: {self.run.run_number} / dataset: {self.primary_dataset} / histo: {self.title}"

    #def save(self, *args, **kwargs):
    #    self.mean = 0 # compute the mean of the array here
    #    self.std  = 0 # compute the std of the array here
    #    super(Histo1DRun, self).save(*args, **kwargs)

    #def extract_features(self, *args, **kwargs):
    #    self.entropy     = 0 # compute additional features here
    #    self.wasserstein = 0

    #def plot(self):
    #    print("Plot 1D histo using matplotlib / js")
