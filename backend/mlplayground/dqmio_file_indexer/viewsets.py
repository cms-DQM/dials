import logging

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from dqmio_celery_tasks.serializers import TaskResponseBase, TaskResponseSerializer
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import FileIndexSerializer, FileIndexInputSerializer
from .models import FileIndex
from .tasks import index_raw_data
from .filters import FileIndexFilter

logger = logging.getLogger(__name__)


class FileIndexViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = FileIndex.objects.all().order_by("st_itime")
    serializer_class = FileIndexSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileIndexFilter

    @extend_schema(
        request=FileIndexInputSerializer,
        responses={200: TaskResponseSerializer}
    )
    @action(
        detail=False,
        methods=["post"],
        name="Search files in DQMIO storages and index",
        url_path=r"ingest",
        pagination_class=None
    )
    def search_files_and_index(self, request):
        task = index_raw_data.delay()
        task = TaskResponseBase(id=task.id, state=task.state, ready=task.ready())
        task = TaskResponseSerializer(task)
        return Response(task.data)
