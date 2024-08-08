import logging
from typing import ClassVar

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from lumisection.models import Lumisection
from rest_framework import mixins, viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from th1.models import TH1
from th2.models import TH2
from utils.db_router import GenericViewSetRouter
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakClientSecretAuthentication,
    CERNKeycloakConfidentialAuthentication,
)

from .filters import MEsFilter
from .models import MEs
from .serializers import MEsSerializer, MinifiedMEsSerializer


logger = logging.getLogger(__name__)


@method_decorator(cache_page(settings.CACHE_TTL), name="retrieve")
@method_decorator(cache_page(settings.CACHE_TTL), name="list")
@method_decorator(vary_on_headers(settings.WORKSPACE_HEADER), name="retrieve")
@method_decorator(vary_on_headers(settings.WORKSPACE_HEADER), name="list")
class MEsViewSet(GenericViewSetRouter, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = MEs.objects.all().order_by(MEs._meta.pk.name)
    serializer_class = MEsSerializer
    filterset_class = MEsFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]
    pagination_class = None

    @action(
        detail=False,
        methods=["GET"],
        url_path=r"(?P<dataset_id>\d+)/(?P<run_number>\d+)",
    )
    def get_run_mes(self, request, dataset_id=None, run_number=None):
        try:
            dataset_id = int(dataset_id)
            run_number = int(run_number)
        except ValueError as err:
            raise ValidationError("dataset_id, run_number, ls_number and me_id must be valid integers.") from err

        workspace = self.get_workspace()
        lumi = (
            Lumisection.objects.using(workspace)
            .filter(dataset_id=dataset_id, run_number=run_number)
            .order_by("ls_number")
            .first()
        )
        th1_mes = (
            TH1.objects.using(workspace)
            .filter(dataset_id=dataset_id, run_number=run_number, ls_number=lumi.ls_number)
            .values_list("me_id", flat=True)
            .distinct()
        )
        th2_mes = (
            TH2.objects.using(workspace)
            .filter(dataset_id=dataset_id, run_number=run_number, ls_number=lumi.ls_number)
            .values_list("me_id", flat=True)
            .distinct()
        )
        mes_ids = [*th1_mes, *th2_mes]
        mes = MEs.objects.using(workspace).filter(me_id__in=mes_ids).all().order_by(MEs._meta.pk.name)
        serializer = MinifiedMEsSerializer(mes, many=True)
        return Response(serializer.data)
