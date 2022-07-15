import asyncio
import logging
from django.db import models
from django.db.models import UniqueConstraint
from django.forms import ModelForm
from django.conf import settings

from data_taking_objects.models import Run, Lumisection

from histograms.models import (
    RunHistogram,
    LumisectionHistogram1D,
    LumisectionHistogram2D,
)

logger = logging.getLogger(__name__)


async def tcp_client(host, port, message):
    reader, writer = await asyncio.open_connection(host, port)

    logger.info(f"Sending to {host}:{port}: {message!r}")
    writer.write(message.encode())

    data = await reader.read(100)
    logger.debug(f"Received from {host}:{port}: {data.decode()!r}")

    logger.info("Closing the connection")
    writer.close()


class Task(models.Model):
    """
    Model describing a set of training and test data,
    both for runs and lumisections, which are used by Models
    """

    DQM_PLAYGROUND_DS_COMMANDS = {
        "quit": "QUIT",
        "run_pipeline": "RUN_PIPELINE",
    }

    name = models.CharField(max_length=200)
    training_runs = models.ManyToManyField(
        Run,
        help_text="Runs used as a whole for training the model",
        blank=True,
        related_name="tasks_using_for_training",
    )
    training_lumisections = models.ManyToManyField(
        Lumisection,
        help_text="Lumisections used for training the model",
        blank=True,
        related_name="tasks_using_for_training",
    )
    testing_runs = models.ManyToManyField(
        Run,
        help_text="Runs used as a whole for testing the model",
        blank=True,
        related_name="tasks_using_for_testing",
    )
    testing_lumisections = models.ManyToManyField(
        Lumisection,
        help_text="Lumisections used for testing the model",
        blank=True,
        related_name="tasks_using_for_testing",
    )
    metadata = models.CharField(  # for now...
        help_text="Extra details that describe the Task", blank=True, max_length=200
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [UniqueConstraint(fields=["name"], name="unique task name")]

    def trigger_pipeline(self):
        """
        Trigger the DS project to run the Kedro pipelines
        """
        logger.debug(
            f"Connecting to {settings.DQM_PLAYGROUND_DS_HOST}:{settings.DQM_PLAYGROUND_DS_PORT}"
        )
        asyncio.run(
            tcp_client(
                settings.DQM_PLAYGROUND_DS_HOST,
                settings.DQM_PLAYGROUND_DS_PORT,
                # f"{self.DQM_PLAYGROUND_DS_COMMANDS['run_pipeline']} {self.id}",
                f"{self.DQM_PLAYGROUND_DS_COMMANDS['run_pipeline']}",
            )
        )



class Strategy(models.Model):
    """
    Model describing the ML Strategy used to make a Prediction, using
    the data contained in a Task
    """

    model = models.CharField(
        max_length=100, help_text="Model used by the Strategy", null=False
    )


class Prediction(models.Model):
    """
    Model describing the prediction made by the Strategy  using the Task
    for training and testing
    """

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="predictions",
        help_text="The Task used to make the prediction",
    )
    strategy = models.ForeignKey(
        Strategy,
        on_delete=models.CASCADE,
        related_name="predictions",
        help_text="The Strategy used to make the prediction",
    )
    run_histograms = models.ManyToManyField(
        RunHistogram,
        blank=True,
        related_name="predictions",
        help_text="Specific RunHistograms used to make the prediction [Optional]",
    )
    lumisection_histograms_1d = models.ManyToManyField(
        LumisectionHistogram1D,
        blank=True,
        related_name="predictions",
        help_text="Specific LumisectionHistogram1D used to make the prediction [Optional]",
    )
    lumisection_histograms_2d = models.ManyToManyField(
        LumisectionHistogram2D,
        blank=True,
        related_name="predictions",
        help_text="Specific LumisectionHistogram2D used to make the prediction [Optional]",
    )
    # prediction_value = models.??????  # Actual prediction
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
