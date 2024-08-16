from typing import ClassVar

from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication
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

    def list(self, request):
        class_name = request.query_params.get("class_name")
        dataset_name = request.query_params.get("dataset_name")
        response = self.rr.get_open_runs(class_name, dataset_name)
        return Response(response)
