from typing import ClassVar

from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakBearerAuthentication,
    CERNKeycloakClientSecretAuthentication,
)

from .client import SimpleOMSClient


class OMSProxyViewSet(viewsets.ViewSet):
    oms = SimpleOMSClient()
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakBearerAuthentication,
    ]

    def list(self, request):
        params = dict(request.query_params)
        endpoint = params.pop("endpoint")[0]
        response = self.oms.query(endpoint, params=params)
        return Response(response)
