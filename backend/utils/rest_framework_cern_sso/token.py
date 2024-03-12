from jose.jwt import get_unverified_claims

from .backends import CERNKeycloakOIDC
from .exceptions import InvalidClient


class CERNKeycloakToken:
    def __init__(self, access_token: str, client: CERNKeycloakOIDC | None) -> None:
        self.access_token = access_token
        self.client = client
        self.unv_claims = get_unverified_claims(access_token)
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
        self.claims = self.client.decode_token(
            self.access_token, {"verify_signature": True, "verify_aud": True, "verify_exp": True}
        )

    def validate(self, valid_aud: list, valid_azp: list) -> None:
        self.check_parties(valid_aud, valid_azp)
        self.decode_and_verify()
        self.is_authenticated = True
