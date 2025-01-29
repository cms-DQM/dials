import json

from jwcrypto import jwt

from .backends import CERNKeycloakOIDC
from .exceptions import InvalidClient, InvalidToken


class CERNKeycloakToken:
    def __init__(self, access_token: str, client: CERNKeycloakOIDC | None) -> None:
        self.access_token = access_token
        self.client = client
        self.unv_claims = self.__extract_unv_claims(access_token)
        self.aud = self.unv_claims["aud"]
        self.azp = self.unv_claims["azp"]
        self.claims = None
        self.is_authenticated = False

    @staticmethod
    def __extract_unv_claims(access_token: str) -> jwt.JWT:
        try:
            decoded_jwt = jwt.JWT(key=None, jwt=access_token)
            return json.loads(decoded_jwt.token.objects.get("payload").decode())
        except ValueError as err:
            raise InvalidToken from err

    def decode_and_verify(self) -> None:
        if self.client is None:
            raise ValueError("Unconfigured keycloak client.")
        self.claims = self.client.decode_token(self.access_token)

    def validate(self) -> None:
        # Check the client is properly set
        if self.client is None:
            raise ValueError("Unconfigured keycloak client.")

        # Check the aud matches the client's client_id
        if self.aud != self.client.client_id:
            raise InvalidClient

        self.claims = self.client.decode_token(self.access_token)
        self.is_authenticated = True
