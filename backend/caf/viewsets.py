from typing import ClassVar

from requests.exceptions import HTTPError
from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakClientSecretAuthentication,
    CERNKeycloakConfidentialAuthentication,
)

from .client import CAF


class CAFViewSet(viewsets.ViewSet):
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]

    def list(self, request):
        class_name = request.query_params.get("class_name")
        kind = request.query_params.get("kind")

        try:
            caf = CAF(class_name, kind)
            response = {**caf.latest, "content": caf.download(latest=True)}
        except HTTPError as err:
            if "404 Client Error" in str(err):
                raise NotFound(detail="CAF entry for given class_name and kind could not be found") from err
            else:
                raise err

        return Response(response)
