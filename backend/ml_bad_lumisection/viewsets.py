import logging
from typing import ClassVar

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from lumisection.models import Lumisection
from ml_models_index.models import MLModelsIndex
from rest_framework import mixins, viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from utils.common import list_to_range
from utils.db_router import GenericViewSetRouter
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakClientSecretAuthentication,
    CERNKeycloakConfidentialAuthentication,
)

from .filters import MLBadLumisectionFilter
from .models import MLBadLumisection
from .serializers import MLBadLumisectionSerializer


logger = logging.getLogger(__name__)
composite_pks = next(filter(lambda x: "primary_key" in x.name, MLBadLumisection._meta.constraints), None)


@method_decorator(cache_page(settings.CACHE_TTL), name="list")
@method_decorator(cache_page(settings.CACHE_TTL), name="get_object")
@method_decorator(vary_on_headers(settings.WORKSPACE_HEADER), name="list")
@method_decorator(vary_on_headers(settings.WORKSPACE_HEADER), name="get_object")
class MLBadLumisectionViewSet(GenericViewSetRouter, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = MLBadLumisection.objects.all().order_by(*composite_pks.fields)
    serializer_class = MLBadLumisectionSerializer
    filterset_class = MLBadLumisectionFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]

    @action(
        detail=False,
        methods=["GET"],
        url_path=r"(?P<model_id>\d+)/(?P<dataset_id>\d+)/(?P<run_number>\d+)/(?P<ls_number>\d+)/(?P<me_id>\d+)",
    )
    def get_object(self, request, model_id=None, dataset_id=None, run_number=None, ls_number=None, me_id=None):
        # Since the MLBadLumisection table in the database has a composite primary key
        # that Django doesn't support, we are defining this method
        # as a custom retrieve method to query this table by the composite primary key
        try:
            model_id = int(model_id)
            dataset_id = int(dataset_id)
            run_number = int(run_number)
            ls_number = int(ls_number)
            me_id = int(me_id)
        except ValueError as err:
            raise ValidationError(
                "model_id, dataset_id, run_number, ls_number and me_id must be valid integers."
            ) from err

        queryset = self.get_queryset()
        queryset = get_object_or_404(
            queryset, model_id=model_id, dataset_id=dataset_id, run_number=run_number, ls_number=ls_number, me_id=me_id
        )
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path=r"cert-json")
    def generate_certificate_json(self, request):
        try:
            dataset_id = int(request.query_params.get("dataset_id"))
            run_number = list(map(int, request.query_params.get("run_number__in").split(",")))
            model_id = list(map(int, request.query_params.get("model_id__in").split(",")))
        except ValueError as err:
            raise ValidationError(
                "dataset_id and run_number must be valid integers and model_ids a valid list of integers"
            ) from err

        # Select user's workspace
        workspace = self.get_workspace()

        # Fetch models' metadata in the given workspace
        models = MLModelsIndex.objects.using(workspace).filter(model_id__in=model_id).all().values()
        models = {qs.get("model_id"): qs for qs in models}

        # Fetch predictions for a given dataset, multiple runs from multiple models
        queryset = self.get_queryset()
        result = (
            queryset.filter(dataset_id=dataset_id, run_number__in=run_number, model_id__in=model_id)
            .all()
            .order_by("run_number", "ls_number")
            .values()
        )
        result = [qs for qs in result]

        # Format bad lumi certification json
        response = {}
        for run in run_number:
            response[run] = {}
            predictions_in_run = [res for res in result if res.get("run_number") == run]
            unique_ls = [res.get("ls_number") for res in predictions_in_run]
            for ls in unique_ls:
                response[run][ls] = []
                predictions_in_ls = [res for res in predictions_in_run if res.get("ls_number") == ls]
                for preds in predictions_in_ls:
                    model_id = preds.get("model_id")
                    me_id = preds.get("me_id")
                    filename = models[model_id].get("filename")
                    target_me = models[model_id].get("target_me")
                    response[run][ls].append(
                        {"model_id": model_id, "me_id": me_id, "filename": filename, "me": target_me}
                    )

        return Response(response)

    @action(detail=False, methods=["GET"], url_path=r"golden-json")
    def generate_golden_json(self, request):
        try:
            dataset_id = int(request.query_params.get("dataset_id"))
            run_number = list(map(int, request.query_params.get("run_number__in").split(",")))
            model_id = list(map(int, request.query_params.get("model_id__in").split(",")))
        except ValueError as err:
            raise ValidationError(
                "dataset_id and run_number must be valid integers and model_ids a valid list of integers"
            ) from err

        # Select user's workspace
        workspace = self.get_workspace()

        # Fetch predictions for a given dataset, multiple runs from multiple models
        queryset = self.get_queryset()
        result = (
            queryset.filter(dataset_id=dataset_id, run_number__in=run_number, model_id__in=model_id)
            .all()
            .order_by("run_number", "ls_number")
            .values()
        )
        result = [qs for qs in result]

        # Generate ML golden json
        response = {}
        for run in run_number:
            queryset = self.get_queryset()
            bad_lumis = (
                queryset.filter(dataset_id=dataset_id, run_number=run, model_id__in=model_id)
                .all()
                .order_by("ls_number")
                .values_list("ls_number", flat=True)
                .distinct()
            )
            bad_lumis = [qs for qs in bad_lumis]
            all_lumis = (
                Lumisection.objects.using(workspace)
                .filter(dataset_id=dataset_id, run_number=run)
                .all()
                .values_list("ls_number", flat=True)
            )
            good_lumis = [ls for ls in all_lumis if ls not in bad_lumis]
            response[run] = list_to_range(good_lumis)

        return Response(response)
