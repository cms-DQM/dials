import json
import logging

from django.conf import settings
from django.http import HttpResponseBadRequest
from drf_spectacular.utils import extend_schema
from keycloak.exceptions import KeycloakPostError
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakPublicAuthentication,
    confidential_kc,
)
from utils.rest_framework_cern_sso.user import CERNKeycloakUser

from .serializers import (
    DeviceCodeSerializer,
    DeviceSerializer,
    DeviceTokenSerializer,
    ExchangedTokenSerializer,
    PendingAuthorizationErrorSerializer,
    RefreshTokenSerializer,
    SubjectTokenSerializer,
)


logger = logging.getLogger(__name__)


class AuthViewSet(ViewSet):
    @extend_schema(
        request=SubjectTokenSerializer,
        responses={200: ExchangedTokenSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        name="Exchange public access token to confidential access_token",
        url_path=r"exchange-token",
        authentication_classes=[CERNKeycloakPublicAuthentication],
    )
    def exchange_token(self, request: Request):
        subject_token = request.data.get("subject_token")
        if not subject_token:
            return HttpResponseBadRequest("Attribute 'subject_token' not found in request body.")

        user: CERNKeycloakUser = request.user
        confidential_token = user.token.client.exchange_token(subject_token, settings.KEYCLOAK_CONFIDENTIAL_CLIENT_ID)
        payload = ExchangedTokenSerializer(confidential_token).data
        return Response(payload)

    @extend_schema(
        request=RefreshTokenSerializer,
        responses={200: DeviceTokenSerializer},
    )
    @action(detail=False, methods=["post"], name="Refresh confidential token", url_path=r"refresh-token")
    def refresh_token(self, request: Request):
        ref_token = request.data.get("refresh_token")
        if not ref_token:
            return HttpResponseBadRequest("Attribute 'refresh_token' not found in request body.")

        confidential_token = confidential_kc.refresh_token(ref_token)
        payload = DeviceTokenSerializer(confidential_token).data
        return Response(payload)

    @extend_schema(
        request=None,
        responses={200: DeviceSerializer},
    )
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

    @extend_schema(
        request=DeviceCodeSerializer,
        responses={200: DeviceTokenSerializer, 400: PendingAuthorizationErrorSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        name="Verify if device code was authenticate and issue token",
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
            if err_msg.get("error") != "authorization_pending":
                raise err
            err_msg = {"detail": err_msg.get("error_description"), "code": err_msg.get("error")}
            payload = PendingAuthorizationErrorSerializer(err_msg).data
            response = Response(payload, status=err.response_code)
        else:
            payload = DeviceTokenSerializer(token).data
            response = Response(payload)

        return response
