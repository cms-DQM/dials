import json
import logging

from django.conf import settings
from django.http import HttpResponseBadRequest
from keycloak.exceptions import KeycloakPostError
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from utils.db_router import get_workspace_from_role
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakClientSecretAuthentication,
    CERNKeycloakConfidentialAuthentication,
    confidential_kc,
)
from utils.rest_framework_cern_sso.token import CERNKeycloakToken
from utils.rest_framework_cern_sso.user import CERNKeycloakUser

from .serializers import (
    ConfiguredWorkspacesSerializer,
    DeviceSerializer,
    DeviceTokenSerializer,
    PendingAuthorizationErrorSerializer,
)


logger = logging.getLogger(__name__)


class AuthViewSet(ViewSet):
    @action(
        detail=False,
        methods=["get"],
        name="Inspect configured workspaces",
        url_path=r"workspaces",
        authentication_classes=[CERNKeycloakClientSecretAuthentication, CERNKeycloakConfidentialAuthentication],
    )
    def get_workspaces(self, request: Request):
        payload = {"workspaces": list(settings.WORKSPACES.keys())}
        payload = ConfiguredWorkspacesSerializer(payload).data
        return Response(payload)

    @action(
        detail=False,
        methods=["get"],
        name="Inspect user default workspace based on their token",
        url_path=r"user-default-workspace",
        authentication_classes=[CERNKeycloakConfidentialAuthentication],
    )
    def get_user_default_workspace(self, request: Request):
        user: CERNKeycloakUser = request.user
        subject_token = user.token.access_token

        token_obj = CERNKeycloakToken(subject_token, client=None)
        cern_roles = token_obj.unv_claims.get("cern_roles")
        ws = get_workspace_from_role(cern_roles, use_default_if_not_found=True)

        payload = {"workspace": ws}
        return Response(payload)

    @action(detail=False, methods=["post"], name="Refresh confidential token", url_path=r"refresh-token")
    def refresh_token(self, request: Request):
        ref_token = request.data.get("refresh_token")
        if not ref_token:
            return HttpResponseBadRequest("Attribute 'refresh_token' not found in request body.")

        confidential_token = confidential_kc.refresh_token(ref_token)
        payload = DeviceTokenSerializer(confidential_token).data
        return Response(payload)

    @action(
        detail=False,
        methods=["get"],
        name="Issue device code",
        url_path=r"new-device",
    )
    def get_device(self, request: Request):
        issue_device = confidential_kc.get_device()
        payload = DeviceSerializer(issue_device).data
        return Response(payload)

    @action(
        detail=False,
        methods=["post"],
        name="Verify if device code was authenticated and issue token",
        url_path=r"device-token",
    )
    def issue_device_token(self, request: Request):
        device_code = request.data.get("device_code")
        if not device_code:
            return HttpResponseBadRequest("Attribute 'device_code' not found in request body.")

        try:
            token = confidential_kc.issue_device_token(device_code=device_code)
        except KeycloakPostError as err:
            err_msg = json.loads(err.error_message.decode("utf-8"))
            err_msg = {"detail": err_msg.get("error_description"), "code": err_msg.get("error")}
            payload = PendingAuthorizationErrorSerializer(err_msg).data
            response = Response(payload, status=err.response_code)
        else:
            payload = DeviceTokenSerializer(token).data
            response = Response(payload)

        return response
