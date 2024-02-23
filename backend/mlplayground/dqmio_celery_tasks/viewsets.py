import logging

from utils.rest_framework_cern_sso.authentication import CERNKeycloakConfidentialAuthentication, CERNKeycloakClientSecretAuthentication
from django_celery_results.models import TaskResult
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from .filters import CeleryTasksFilters
from .serializers import CeleryTasksSerializer

logger = logging.getLogger(__name__)


class CeleryTasksViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Runs metadata
    """

    queryset = TaskResult.objects.all().order_by("-date_done")
    serializer_class = CeleryTasksSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CeleryTasksFilters
    lookup_field = "task_id"
    authentication_classes = [CERNKeycloakClientSecretAuthentication, CERNKeycloakConfidentialAuthentication]
