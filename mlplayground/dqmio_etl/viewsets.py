import logging

from django.http import HttpResponseBadRequest
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from dqmio_celery_tasks.serializers import TaskResponseBase, TaskResponseSerializer
from dqmio_file_indexer.models import FileIndex, FileIndexStatus

from .models import (
    Run,
    Lumisection,
    LumisectionHistogram1D,
    LumisectionHistogram2D,
)
from .serializers import (
    DQMIORunSerializer,
    DQMIOLumisectionSerializer,
    DQMIOLumisectionHistogram1DSerializer,
    DQMIOLumisectionHistogram2DSerializer,
    DQMIOLumisectionHistogramsIngetionInputSerializer
)
from .filters import (
    RunFilter,
    LumisectionFilter,
    LumisectionHistogram1DFilter,
    LumisectionHistogram2DFilter
)
from .tasks import ingest_function

logger = logging.getLogger(__name__)


class DQMIORunViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Runs metadata
    """
    queryset = Run.objects.all().order_by("run_number")
    serializer_class = DQMIORunSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RunFilter


class DQMIOLumisectionViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Lumisections metadata
    """
    queryset = Lumisection.objects.all().order_by("id")
    serializer_class = DQMIOLumisectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LumisectionFilter

    @extend_schema(
        request=DQMIOLumisectionHistogramsIngetionInputSerializer,
        responses={200: TaskResponseSerializer}
    )
    @action(
        detail=False,
        methods=["post"],
        name="Trigger ETL pipeline for histograms at lumisection granularity-level",
        url_path=r"ingest-histograms"
    )
    def run(self, request):
        file_index_id = request.data.get("id")
        if not file_index_id:
            return HttpResponseBadRequest("Attribute 'id' not found in request body.")

        file_index = FileIndex.objects.get(id=file_index_id)
        file_index.update_status(FileIndexStatus.PENDING)
        del file_index

        # Here I'am passing the file_index_id instead of the FileIndex object
        # because functions arguments using celery queue must be JSON serializable
        # and the FileIndex object (django model) is not
        task = ingest_function.delay(file_index_id)
        task = TaskResponseBase(id=task.id, state=task.state, ready=task.ready())
        task = TaskResponseSerializer(task)
        return Response(task.data)


class DQMIOLumisectionHistogram1DViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested 1d-histograms at lumisection granularity-level
    """
    queryset = LumisectionHistogram1D.objects.all().order_by("id")
    serializer_class = DQMIOLumisectionHistogram1DSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LumisectionHistogram1DFilter


class DQMIOLumisectionHistogram2DViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested 2d-histograms at lumisection granularity-level
    """
    queryset = LumisectionHistogram2D.objects.all().order_by("id")
    serializer_class = DQMIOLumisectionHistogram2DSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LumisectionHistogram2DFilter
