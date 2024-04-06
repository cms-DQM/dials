import logging
from typing import ClassVar

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.authentication import BaseAuthentication
from utils.db_router import GenericViewSetRouter
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
from .models import (
    Lumisection,
    LumisectionHistogram1D,
    LumisectionHistogram1DMEs,
    LumisectionHistogram2D,
    LumisectionHistogram2DMEs,
    Run,
)
from .serializers import (
    LumisectionHistogram1DMEsSerializer,
    LumisectionHistogram1DSerializer,
    LumisectionHistogram2DMEsSerializer,
    LumisectionHistogram2DSerializer,
    LumisectionSerializer,
    RunSerializer,
)


logger = logging.getLogger(__name__)


class RunViewSet(GenericViewSetRouter, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
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


class LumisectionViewSet(
    GenericViewSetRouter, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    You can see all ingested Lumisections metadata
    """

    queryset = Lumisection.objects.all().order_by("ls_id")
    serializer_class = LumisectionSerializer
    filterset_class = LumisectionFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]


class LumisectionHistogram1DMEsViewSet(GenericViewSetRouter, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LumisectionHistogram1DMEs.objects.all().order_by("title")
    serializer_class = LumisectionHistogram1DMEsSerializer
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]
    pagination_class = None


class LumisectionHistogram1DViewSet(
    GenericViewSetRouter, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    You can see all ingested 1d-histograms at lumisection granularity-level
    """

    # If we need to return the fields from dqmio_index and lumisection tables
    # we can update the serializer and add select_related to this queryset:
    # .select_related('ls_id').select_related('file_id')

    # This will ensure all requests will JOIN the tables and extract the fields
    # on the serializer we add:
    # ls_number = serializers.IntegerField(source="ls_id.ls_number")
    # era = serializers.CharField(source="file_id.era")

    # If we don't add the "select_related" here the serializer will do a query for each
    # element returned by the queryset

    queryset = LumisectionHistogram1D.objects.all().order_by("hist_id")
    serializer_class = LumisectionHistogram1DSerializer
    filterset_class = LumisectionHistogram1DFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]


class LumisectionHistogram2DMEsViewSet(GenericViewSetRouter, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LumisectionHistogram2DMEs.objects.all().order_by("title")
    serializer_class = LumisectionHistogram2DMEsSerializer
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]
    pagination_class = None


class LumisectionHistogram2DViewSet(
    GenericViewSetRouter, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    You can see all ingested 2d-histograms at lumisection granularity-level
    """

    queryset = LumisectionHistogram2D.objects.all().order_by("hist_id")
    serializer_class = LumisectionHistogram2DSerializer
    filterset_class = LumisectionHistogram2DFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]
