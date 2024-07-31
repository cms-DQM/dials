from datetime import datetime, timedelta

import requests
import urllib3
from django.conf import settings
from utils.rest_framework_cern_sso.backends import CERNKeycloakOIDC


class SimpleOMSClient:
    OMS_API_URL = "https://cmsoms.cern.ch/agg/api/v1"
    OMS_AUDIENCE = "cmsoms-prod"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.kc = CERNKeycloakOIDC(
            skip_pk=True,
            server_url=settings.KEYCLOAK_SERVER_URL,
            realm_name=settings.KEYCLOAK_REALM,
            client_id=settings.OMS_SSO_CLIENT_ID,
            client_secret_key=settings.OMS_SSO_CLIENT_SECRET,
        )
        self.auth = None
        self.expires_at = None

    def __auth(self):
        token = self.kc.issue_api_token(aud=self.OMS_AUDIENCE)
        self.expires_at = datetime.now() + timedelta(seconds=token["expires_in"])
        self.auth = f"{token['token_type']} {token['access_token']}"

    def __is_expired(self):
        if self.expires_at is None:
            return True
        return (self.expires_at - timedelta(seconds=15)) < datetime.now()

    def __build_headers(self):
        if self.__is_expired():
            self.__auth()
        return {"Authorization": self.auth, "Content-type": "application/json"}

    def query(self, endpoint: str, **kwargs):
        headers = self.__build_headers()

        # Running this curl request from LXPlus works without -k flag
        # This is here to avoid double requesting OMS
        # since the application is deployed in Openshift
        with urllib3.warnings.catch_warnings():
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(
                f"{self.OMS_API_URL}/{endpoint}",
                headers=headers,
                timeout=self.timeout,
                verify=False,  # noqa: S501
                **kwargs,
            )

        response.raise_for_status()
        return response.json()
