import logging
from typing import ClassVar

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from utils.db_router import GenericViewSetRouter
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakBearerAuthentication,
    CERNKeycloakClientSecretAuthentication,
)

from .filters import TH2Filter
from .models import TH2
from .serializers import TH2Serializer


logger = logging.getLogger(__name__)
composite_pks = next(filter(lambda x: "primary_key" in x.name, TH2._meta.constraints), None)


@method_decorator(cache_page(settings.CACHE_TTL), name="get_object")
@method_decorator(cache_page(settings.CACHE_TTL), name="list")
@method_decorator(vary_on_headers(settings.WORKSPACE_HEADER), name="get_object")
@method_decorator(vary_on_headers(settings.WORKSPACE_HEADER), name="list")
class TH2ViewSet(GenericViewSetRouter, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = TH2.objects.all().order_by(*composite_pks.fields)
    serializer_class = TH2Serializer
    filterset_class = TH2Filter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakBearerAuthentication,
    ]

    @action(
        detail=False,
        methods=["GET"],
        url_path=r"(?P<dataset_id>\d+)/(?P<run_number>\d+)/(?P<ls_number>\d+)/(?P<me_id>\d+)",
    )
    def get_object(self, request, dataset_id=None, run_number=None, ls_number=None, me_id=None):
        # Since the TH2 table in the database has a composite primary key
        # that Django doesn't support, we are defining this method
        # as a custom retrieve method to query this table by the composite primary key
        try:
            dataset_id = int(dataset_id)
            run_number = int(run_number)
            ls_number = int(ls_number)
            me_id = int(me_id)
        except ValueError as err:
            raise ValidationError("dataset_id, run_number, ls_number and me_id must be valid integers.") from err

        queryset = self.get_queryset()
        queryset = get_object_or_404(
            queryset, dataset_id=dataset_id, run_number=run_number, ls_number=ls_number, me_id=me_id
        )
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)
