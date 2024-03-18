import logging
from typing import ClassVar

from django.conf import settings
from django.db.models import Count, F, TextField, Value
from django.http import HttpResponseBadRequest
from django_filters.rest_framework import DjangoFilterBackend
from dqmio_celery_tasks.serializers import TaskResponseBase, TaskResponseSerializer
from dqmio_file_indexer.models import FileIndex, FileIndexStatus
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakClientSecretAuthentication,
    CERNKeycloakConfidentialAuthentication,
)

from .filters import (
    LumisectionFilter,
    LumisectionHistogram1DFilter,
    LumisectionHistogram2DFilter,
    RunFilter,
)
from .models import Lumisection, LumisectionHistogram1D, LumisectionHistogram2D, Run
from .serializers import (
    LumisectionHistogram1DSerializer,
    LumisectionHistogram2DSerializer,
    LumisectionHistogramsIngestionInputSerializer,
    LumisectionHistogramsSubsystemCountSerializer,
    LumisectionSerializer,
    MEsSerializer,
    RunLumisectionsSerializer,
    RunSerializer,
)
from .tasks import ingest_function
from .utils import SplitPart, paginate


logger = logging.getLogger(__name__)


class RunViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Runs metadata
    """

    queryset = Run.objects.all().order_by("run_number")
    serializer_class = RunSerializer
    filterset_class = RunFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]

    @extend_schema(
        responses={200: RunLumisectionsSerializer(many=True)},
    )
    @paginate(page_size=10, serializer_class=RunLumisectionsSerializer)
    @action(
        detail=True,
        methods=["get"],
        name="Get all lumisections inside a Run",
        url_path=r"lumisections",
        filterset_class=None,
    )
    def list_lumisection(self, request, pk=None):
        result = []
        lumis = Lumisection.objects.filter(run_id=pk)
        for lumi in lumis:
            result.append(
                {
                    "id": lumi.id,
                    "ls_number": lumi.ls_number,
                    "hist1d_count": lumi.dqmio_etl_lumisectionhistogram1d_histograms.count(),
                    "hist2d_count": lumi.dqmio_etl_lumisectionhistogram2d_histograms.count(),
                    "int_lumi": None,
                    "oms_zerobias_rate": lumi.oms_zerobias_rate,
                }
            )
        return result


class LumisectionViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Lumisections metadata
    """

    queryset = Lumisection.objects.all().order_by("id")
    serializer_class = LumisectionSerializer
    filterset_class = LumisectionFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]

    @extend_schema(
        request=LumisectionHistogramsIngestionInputSerializer,
        responses={200: TaskResponseSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        name="Trigger ETL pipeline for histograms at lumisection granularity-level",
        url_path=r"ingest-histograms",
    )
    def run(self, request):
        file_index_id = request.data.get("id")
        if not file_index_id:
            return HttpResponseBadRequest("Attribute 'id' not found in request body.")

        queue = request.data.get("queue")
        if not queue:
            return HttpResponseBadRequest("Attribute 'queue' not found in request body.")

        file_index = FileIndex.objects.get(id=file_index_id)
        file_index.update_status(FileIndexStatus.PENDING)
        del file_index

        # Here I'am passing the file_index_id instead of the FileIndex object
        # because functions arguments using celery queue must be JSON serializable
        # and the FileIndex object (django model) is not
        task = ingest_function.apply_async(kwargs={"file_index_id": file_index_id}, queue=queue)
        task = TaskResponseBase(task_id=task.id, state=task.state, ready=task.ready())
        task = TaskResponseSerializer(task)
        return Response(task.data)

    @extend_schema(
        request=None,
        responses={200: MEsSerializer},
    )
    @action(
        detail=False,
        methods=["get"],
        name="List filtered MEs during ETL",
        url_path=r"configured-mes",
    )
    def configured_mes(self, request):
        payload = MEsSerializer({"mes": settings.DQMIO_MES_TO_INGEST})
        return Response(payload.data)


class LumisectionHistogram1DViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested 1d-histograms at lumisection granularity-level
    """

    queryset = LumisectionHistogram1D.objects.all().order_by("id")
    serializer_class = LumisectionHistogram1DSerializer
    filterset_class = LumisectionHistogram1DFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]

    @extend_schema(responses={200: LumisectionHistogramsSubsystemCountSerializer(many=True)})
    @action(
        detail=False,
        methods=["get"],
        name="Get number of h1d ingested by subsystem",
        url_path=r"count-by-subsystem",
        pagination_class=False,
        filterset_class=False,
    )
    def count_by_subsystem(self, request):
        subsystem = SplitPart(F("title"), Value("/"), 1, output_field=TextField())
        data = (
            LumisectionHistogram1D.objects.annotate(subsystem=subsystem)
            .values("subsystem")
            .annotate(count=Count("subsystem"))
            .order_by()
        )
        data = list(data)
        return Response(data)


class LumisectionHistogram2DViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested 2d-histograms at lumisection granularity-level
    """

    queryset = LumisectionHistogram2D.objects.all().order_by("id")
    serializer_class = LumisectionHistogram2DSerializer
    filterset_class = LumisectionHistogram2DFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]

    @extend_schema(responses={200: LumisectionHistogramsSubsystemCountSerializer(many=True)})
    @action(
        detail=False,
        methods=["get"],
        name="Get number of h2d ingested by subsystem",
        url_path=r"count-by-subsystem",
        pagination_class=False,
        filterset_class=False,
    )
    def count_by_subsystem(self, request):
        subsystem = SplitPart(F("title"), Value("/"), 1, output_field=TextField())
        data = (
            LumisectionHistogram2D.objects.annotate(subsystem=subsystem)
            .values("subsystem")
            .annotate(count=Count("subsystem"))
            .order_by()
        )
        data = list(data)
        return Response(data)
