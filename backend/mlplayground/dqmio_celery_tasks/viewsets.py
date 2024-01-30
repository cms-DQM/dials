import logging

from django_celery_results.models import TaskResult
from drf_spectacular.utils import extend_schema
from mlplayground import celery_app
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CeleryTasksSerializer, InspectResponseBase, InspectResponseSerializer

logger = logging.getLogger(__name__)
inspect = celery_app.control.inspect()


class CeleryTasksViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Runs metadata
    """

    queryset = TaskResult.objects.all().order_by("-date_done")
    serializer_class = CeleryTasksSerializer
    lookup_field = "task_id"

    @extend_schema(
        request=None,
        responses={200: InspectResponseSerializer(many=True)},
    )
    @action(
        detail=False,
        methods=["get"],
        name="List received tasks waiting to start",
        url_path=r"queued",
        pagination_class=None,
    )
    def check_queued_tasks(self, request):
        result = []
        for worker, tasks in inspect.reserved().items():
            for task in tasks:
                result.append(
                    InspectResponseBase(
                        id=task.get("id"),
                        name=task.get("name"),
                        queue=task.get("delivery_info", {}).get("routing_key"),
                        worker=worker,
                    )
                )

        result = InspectResponseSerializer(result, many=True)
        return Response(result.data)
