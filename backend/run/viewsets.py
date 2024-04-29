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
    CERNKeycloakClientSecretAuthentication,
    CERNKeycloakConfidentialAuthentication,
)

from .filters import RunFilter
from .models import Run
from .serializers import RunSerializer


logger = logging.getLogger(__name__)
composite_pks = next(filter(lambda x: "primary_key" in x.name, Run._meta.constraints), None)


@method_decorator(cache_page(settings.CACHE_TTL), name="list")
@method_decorator(cache_page(settings.CACHE_TTL), name="get_object")
@method_decorator(vary_on_headers(settings.WORKSPACE_HEADER), name="list")
@method_decorator(vary_on_headers(settings.WORKSPACE_HEADER), name="get_object")
class RunViewSet(GenericViewSetRouter, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Run.objects.all().order_by(*composite_pks.fields)
    serializer_class = RunSerializer
    filterset_class = RunFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]

    @action(
        detail=False,
        methods=["GET"],
        url_path=r"(?P<dataset_id>\d+)/(?P<run_number>\d+)",
    )
    def get_object(self, request, dataset_id=None, run_number=None):
        # Since the Run table in the database has a composite primary key
        # that Django doesn't support, we are defining this method
        # as a custom retrieve method to query this table by the composite primary key
        try:
            dataset_id = int(dataset_id)
            run_number = int(run_number)
        except ValueError as err:
            raise ValidationError("dataset_id and run_number must be valid integers.") from err

        queryset = self.get_queryset()
        queryset = get_object_or_404(queryset, dataset_id=dataset_id, run_number=run_number)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path=r"count",
    )
    def count(self, request):
        count = self.filter_queryset(self.get_queryset()).count()
        return Response({"count": count})
