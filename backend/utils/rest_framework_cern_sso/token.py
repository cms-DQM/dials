import json

from jwcrypto import jwt

from .backends import CERNKeycloakOIDC
from .exceptions import InvalidClient


class CERNKeycloakToken:
    def __init__(self, access_token: str, client: CERNKeycloakOIDC | None) -> None:
        self.access_token = access_token
        self.client = client
        decoded_jwt = jwt.JWT(key=None, jwt=access_token)
        self.unv_claims = json.loads(decoded_jwt.token.objects.get("payload").decode())
        self.aud = self.unv_claims["aud"]
        self.azp = self.unv_claims["azp"]
        self.claims = None
        self.is_authenticated = False

    def check_parties(self, valid_aud: list, valid_azp: list) -> None:
        if self.aud not in valid_aud:
            raise InvalidClient
        if self.azp not in valid_azp:
            raise InvalidClient

    def decode_and_verify(self) -> None:
        if self.client is None:
            raise ValueError("Unconfigured keycloak client.")
        self.claims = self.client.decode_token(self.access_token)

    def validate(self, valid_aud: list, valid_azp: list) -> None:
        self.check_parties(valid_aud, valid_azp)
        self.decode_and_verify()
        self.is_authenticated = True
