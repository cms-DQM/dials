import logging

from django.http import HttpResponseBadRequest
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from dqmio_celery_tasks.serializers import TaskResponseBase, TaskResponseSerializer

from .models import (
    Run,
    Lumisection,
    RunHistogram,
    LumisectionHistogram1D,
    LumisectionHistogram2D,
)
from .serializers import (
    DQMIORunSerializer,
    DQMIOLumisectionSerializer,
    DQMIORunHistogramSerializer,
    DQMIOLumisectionHistogram1DSerializer,
    DQMIOLumisectionHistogram2DSerializer,
    DQMIOLumisectionHistogram1DInputSerializer,
    DQMIOLumisectionHistogram2DInputSerializer,
)
from .tasks import h1d_ingest_function, h2d_ingest_function

logger = logging.getLogger(__name__)


class DQMIORunViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Runs metadata
    """
    queryset = Run.objects.all().order_by("run_number")
    serializer_class = DQMIORunSerializer


class DQMIOLumisectionViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Lumisections metadata
    """
    queryset = Lumisection.objects.all().order_by("id")
    serializer_class = DQMIOLumisectionSerializer


class DQMIORunHistogramViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested histograms at run granularity-level
    """
    queryset = RunHistogram.objects.all().order_by("id")
    serializer_class = DQMIORunHistogramSerializer

    # TODO
    # Action to trigger ETL pipeline for histograms at run granularity-level


class DQMIOLumisectionHistogram1DViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested 1d-histograms at lumisection granularity-level
    """
    queryset = LumisectionHistogram1D.objects.all().order_by("id")
    serializer_class = DQMIOLumisectionHistogram1DSerializer

    @extend_schema(
        request=DQMIOLumisectionHistogram1DInputSerializer,
        responses={200: TaskResponseSerializer}
    )
    @action(
        detail=False,
        methods=["post"],
        name="Trigger ETL pipeline for 1d-histograms at lumisection granularity-level",
        url_path=r"ingest"
    )
    def run(self, request):
        file_index_id = request.data.get("id")
        if not file_index_id:
            return HttpResponseBadRequest("Attribute 'id' not found in request body.")

        task = h1d_ingest_function.delay(file_index_id)
        task = TaskResponseBase(id=task.id, state=task.state, ready=task.ready())
        task = TaskResponseSerializer(task)
        return Response(task.data)


class DQMIOLumisectionHistogram2DViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested 2d-histograms at lumisection granularity-level
    """
    queryset = LumisectionHistogram2D.objects.all().order_by("id")
    serializer_class = DQMIOLumisectionHistogram2DSerializer

    @extend_schema(
        request=DQMIOLumisectionHistogram2DInputSerializer,
        responses={200: TaskResponseSerializer}
    )
    @action(
        detail=False,
        methods=["post"],
        name="Trigger ETL pipeline for 2d-histograms at lumisection granularity-level",
        url_path=r"ingest"
    )
    def run(self, request):
        file_index_id = request.data.get("id")
        read_chunk_lumi = request.data.get("readUntilLumi", -1)
        if not file_index_id:
            return HttpResponseBadRequest("Attribute 'id' not found in request body.")

        task = h2d_ingest_function.delay(file_index_id, read_chunk_lumi)
        task = TaskResponseBase(id=task.id, state=task.state, ready=task.ready())
        task = TaskResponseSerializer(task)
        return Response(task.data)
