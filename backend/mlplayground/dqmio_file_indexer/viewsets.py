import logging

from custom_auth.keycloak import KeycloakAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from .filters import FileIndexFilter
from .models import FileIndex
from .serializers import FileIndexSerializer

logger = logging.getLogger(__name__)


class FileIndexViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = FileIndex.objects.all().order_by("st_itime")
    serializer_class = FileIndexSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileIndexFilter
    authentication_classes = [KeycloakAuthentication]
