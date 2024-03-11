import requests
from keycloak import KeycloakOpenID

from .exceptions import KeycloakClientError


class CERNKeycloakOIDC:
    def __init__(self, skip_pk: bool = False, **kwargs) -> None:
        self.server_url: str = kwargs["server_url"]
        self.realm_name: str = kwargs["realm_name"]
        self.client_id: str = kwargs["client_id"]
        self.client_secret_key: str | None = kwargs.get("client_secret_key")
        self._kc = KeycloakOpenID(**kwargs)
        self.skip_pk = skip_pk

        if self.skip_pk is False:
            self.public_key = self.__build_public_key()

    def __build_public_key(self) -> str:
        return "-----BEGIN PUBLIC KEY-----\n" + self._kc.public_key() + "\n-----END PUBLIC KEY-----"

    def issue_user_token(self, username: str, password: str, totp: str | None = None) -> dict:
        return self._kc.token(username, password, totp=totp)

    def issue_device_token(self, device_code: str) -> dict:
        return self._kc.token(grant_type="urn:ietf:params:oauth:grant-type:device_code", device_code=device_code)

    def issue_api_token(self) -> dict:
        response = requests.post(
            f"{self.server_url}realms/{self.realm_name}/api-access/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret_key,
                "audience": self.client_id,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get_device(self) -> dict:
        return self._kc.device()

    def decode_token(self, token: str, options: dict) -> dict:
        if self.skip_pk is True:
            raise KeycloakClientError
        options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
        return self._kc.decode_token(token, key=self.public_key, options=options)

    def exchange_token(self, subject_token: str, target_aud: str) -> dict:
        return self._kc.exchange_token(subject_token, target_aud)

    def refresh_token(self, refresh_token: str) -> dict:
        return self._kc.refresh_token(refresh_token)

    def get_user_info(self, token: str) -> dict:
        return self._kc.userinfo(token)
