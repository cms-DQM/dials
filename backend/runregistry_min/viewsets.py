from typing import ClassVar

from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakClientSecretAuthentication,
    CERNKeycloakConfidentialAuthentication,
)

from .client import RunRegistry


class RunRegistryViewSet(viewsets.ViewSet):
    rr = RunRegistry()
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]

    @action(detail=False, methods=["GET"], url_path="editable-datasets")
    def fetch_offline_editable_datasets(self, request):
        class_name = request.query_params.get("class_name")
        dataset_name = request.query_params.get("dataset_name")
        global_state = request.query_params.get("global_state")
        response = self.rr.editable_datasets(class_name, dataset_name, global_state)
        return Response(response)
