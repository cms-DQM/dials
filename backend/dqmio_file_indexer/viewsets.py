import logging
from typing import ClassVar

from django_filters.rest_framework import DjangoFilterBackend
from dqmio_celery_tasks.serializers import TaskResponseBase, TaskResponseSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakClientSecretAuthentication,
    CERNKeycloakConfidentialAuthentication,
)

from .filters import BadFileIndexFilter, FileIndexFilter
from .models import BadFileIndex, FileIndex
from .serializers import BadFileIndexSerializer, FileIndexSerializer
from .tasks import index_files_and_schedule_hists


logger = logging.getLogger(__name__)


class FileIndexViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = FileIndex.objects.all().order_by("st_itime")
    serializer_class = FileIndexSerializer
    filterset_class = FileIndexFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]

    @extend_schema(
        request=None,
        responses={200: TaskResponseSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        name="Trigger file indexing and automatic ingestion schedule",
        url_path=r"index-and-ingest",
    )
    def run(self, request):
        task = index_files_and_schedule_hists.delay()
        task = TaskResponseBase(task_id=task.id, state=task.state, ready=task.ready())
        task = TaskResponseSerializer(task)
        return Response(task.data)


class BadFileIndexViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BadFileIndex.objects.all().order_by("st_itime")
    serializer_class = BadFileIndexSerializer
    filterset_class = BadFileIndexFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]
