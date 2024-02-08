import logging

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseServerError
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from utils.cern_keycloak import InvalidToken, Keycloak

from .keycloak import KeycloakApiTokenAuthentication
from .serializers import ExchangeTokenInputSerializer, ExchangeTokenResponseSerializer, IssueApiTokenResponseSerializer

logger = logging.getLogger(__name__)

kc = Keycloak(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_PUBLIC_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
)


class KeycloakExchangeViewSet(ViewSet):
    """
    View for dealing with keycloak tokens
    """

    serializer_class = ExchangeTokenInputSerializer

    @extend_schema(responses={200: ExchangeTokenResponseSerializer})
    def create(self, request):
        """
        Exchange app client token to api client token
        """
        subject_token = request.data.get("subject_token")
        if not subject_token:
            return HttpResponseBadRequest("Attribute 'subject_token' not found in request body.")

        try:
            kc.validate_audience(subject_token)
        except InvalidToken:
            return HttpResponseBadRequest("Invalid token, audience mismatch.")

        try:
            kc.decode_token(subject_token)
        except Exception:
            return HttpResponseBadRequest("Invalid token, impossible to decode.")

        try:
            target_token = kc.exchange_token(subject_token, settings.KEYCLOAK_CONFIDENTIAL_CLIENT_ID)
        except Exception:
            return HttpResponseServerError("Failed to exchange token.")

        payload = ExchangeTokenResponseSerializer(target_token).data
        return Response(payload)


class KeycloakApiTokenViewSet(ViewSet):
    """
    View for issuing api tokens
    """

    authentication_classes = [KeycloakApiTokenAuthentication]

    @extend_schema(
        request=None,
        responses={200: IssueApiTokenResponseSerializer},
    )
    def create(self, request):
        """
        Exchange app client token to api client token
        """
        target_token = request.user.token
        payload = IssueApiTokenResponseSerializer(target_token).data
        return Response(payload)
