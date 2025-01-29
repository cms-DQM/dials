from typing import ClassVar

from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakBearerAuthentication,
    CERNKeycloakClientSecretAuthentication,
)

from .client import CAF


class CAFViewSet(viewsets.ViewSet):
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakBearerAuthentication,
    ]

    def list(self, request):
        class_name = request.query_params.get("class_name")
        kind = request.query_params.get("kind")
        caf = CAF(class_name, kind)
        response = {**caf.latest, "content": caf.download(latest=True)}
        return Response(response)
