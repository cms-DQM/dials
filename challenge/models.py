from django.db import models
from data_taking_objects.models import Run, Lumisection
from histograms.models import RunHistogram, LumisectionHistogram1D, LumisectionHistogram2D


class Task(models.Model):
    """
    Model describing a set of training and test data, 
    both for runs and lumisections, which are used by Models
    """
    training_runs = models.ManyToManyField(
        Run, help_text="Runs used as a whole for training the model")
    training_lumisections = models.ManyToManyField(
        Lumisection, help_text="Lumisections used for training the model")
    testing_runs = models.ManyToManyField(
        Run, help_text="Runs used as a whole for testing the model")
    testing_lumisections = models.ManyToManyField(
        Lumisection, help_text="Lumisections used for testing the model")


class MLModel(models.Model):
    """
    Model describing the ML Model used to make a Prediction, using
    the data contained in a Task
    """


class Prediction(models.Model):
    """
    Model describing the prediction made by the MLModel, using the Task
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE)
    run_histograms = models.ManyToManyField(RunHistogram,
                                            on_delete=models.CASCADE)
    lumisection_histograms_1d = models.ManyToManyField(
        LumisectionHistogram1D, on_delete=models.CASCADE)
    lumisection_histograms_2d = models.ManyToManyField(
        LumisectionHistogram2D, on_delete=models.CASCADE)

    # prediction = models.??????  # Actual prediction
