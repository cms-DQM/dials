from importlib import util as importlib_util

from django.conf import settings
from jwcrypto.jws import InvalidJWSSignature
from jwcrypto.jwt import JWTExpired, JWTNotYetValid
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from .backends import CERNKeycloakOIDC
from .exceptions import AuthenticationFailed, InvalidToken
from .token import CERNKeycloakToken
from .user import CERNKeycloakUser


if importlib_util.find_spec("drf_spectacular"):
    try:
        from .schemes import *  # noqa: F401,F403
    except ImportError:
        pass

confidential_kc = CERNKeycloakOIDC(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_SECRET_KEY,
    realm_name=settings.KEYCLOAK_REALM,
)

api_clients_kc = {
    client_secret_key: CERNKeycloakOIDC(
        server_url=settings.KEYCLOAK_SERVER_URL,
        client_id=client_id,
        client_secret_key=client_secret_key,
        realm_name=settings.KEYCLOAK_REALM,
    )
    for client_secret_key, client_id in settings.KEYCLOAK_API_CLIENTS.items()
}


class CERNKeycloakClientSecretAuthentication(BaseAuthentication):
    """
    Custom authentication class based on CERN's Keycloak Api Access.

    This authentication flow is solely for authenticating using other confidential clients secret key.
    Those clients must have configured the option
    "My application will need to get tokens using its own client ID and secret".

    What is the use case?
        * Automated scripts that needs non-interactively authentication

    Why not use this authentication for human-users access the api?
        * Because the token generated from "Api Access" do not carry the user information,
        it instead carry general information from the client. That means the users are indistinguishable,
        so you cannot rely on roles unless you create multiple clients for specific roles.
        * Also it is very insecure, because users would share the same secret,
        if one leaks you need to notify all users that you changing the secret key. You could circumvent
        this creating one client per user but that would generate a tons of clients
        and you would also need to clean old clients when users leave cern and loose access to the application.
    """

    HEADER_KEY = "X-CLIENT-SECRET"

    def authenticate(self, request: Request) -> tuple[CERNKeycloakUser, CERNKeycloakToken] | None:
        secret_key = self.get_secret_key(request.headers)

        # Returning None since Django's multi authentication logic
        # works if all N-1 ordered authentication classes
        # return None instead of raising an error
        if secret_key is None:
            return None

        if secret_key not in api_clients_kc:
            raise InvalidToken

        kc: CERNKeycloakOIDC = api_clients_kc[secret_key]
        issued_token = kc.issue_api_token()
        token = CERNKeycloakToken(issued_token["access_token"], kc)

        # We don't need to `validate` because the token was just generated
        # patching the token class for the user class appear validated
        token.is_authenticated = True
        token.claims = token.unv_claims

        return CERNKeycloakUser(token), token

    def get_secret_key(self, headers: dict) -> str:
        return headers.get(self.HEADER_KEY)


class CERNKeycloakBearerAuthentication(BaseAuthentication):
    """
    Custom authentication class based on CERN's Keycloak Bearer Token.

    This authentication flow requires a Bearer token generated from a valid CERN user account
    issued against the configured confidential client of this application or exchanges from
    a trusted client.

    What is the use case?
        * Accepting api requests from frontend services exchanged from the trusted frontend application client.
        * Accepting api requests from scripts through the device authentication flow.
    """

    HEADER_KEY = "Authorization"

    def authenticate(self, request: Request) -> tuple[CERNKeycloakUser, CERNKeycloakToken] | None:
        access_token = self.get_access_token(request.headers)
        token = CERNKeycloakToken(access_token, confidential_kc)

        try:
            token.validate()
        except InvalidJWSSignature as err:
            raise AuthenticationFailed(
                "Found and invalid jws signature while decoding the access token.", "access_token_invalid_jws_signature"
            ) from err
        except JWTExpired as err:
            raise AuthenticationFailed("Access token has expired.", "access_token_expired") from err
        except JWTNotYetValid as err:
            raise AuthenticationFailed("Access token not yet valid.", "access_token_not_yet_valid") from err
        except Exception as err:  # noqa: BLE001
            raise AuthenticationFailed("Unexpected error validating token.", "access_token_unexpected_error") from err

        return CERNKeycloakUser(token), token

    def get_access_token(self, headers: dict) -> str:
        try:
            bearer = headers[self.HEADER_KEY]
        except KeyError as err:
            raise AuthenticationFailed("Authorization header not found.", "authorization_not_found") from err

        try:
            return bearer.split("Bearer ")[-1]
        except AttributeError as err:
            raise AuthenticationFailed("Malformed access token.", "bad_access_token") from err
