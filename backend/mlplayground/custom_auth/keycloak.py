from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from jose import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from utils.cern_keycloak import Keycloak

kc = {
    settings.KEYCLOAK_CONFIDENTIAL_CLIENT_ID: Keycloak(
        server_url=settings.KEYCLOAK_SERVER_URL,
        client_id=settings.KEYCLOAK_CONFIDENTIAL_CLIENT_ID,
        client_secret_key=settings.KEYCLOAK_CONFIDENTIAL_SECRET_KEY,
        realm_name=settings.KEYCLOAK_REALM,
    ),
    **{
        client_id: Keycloak(
            server_url=settings.KEYCLOAK_SERVER_URL,
            client_id=client_id,
            client_secret_key=client_secret_key,
            realm_name=settings.KEYCLOAK_REALM,
        )
        for client_secret_key, client_id in settings.KEYCLOAK_API_CLIENTS.items()
    },
}
api_clients = list(settings.KEYCLOAK_API_CLIENTS.values())
valid_clients = [settings.KEYCLOAK_CONFIDENTIAL_CLIENT_ID, settings.KEYCLOAK_PUBLIC_CLIENT_ID, *api_clients]


class KeycloakUser(AnonymousUser):
    """
    Django Rest Framework needs an user to consider authenticated
    """

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info

    @property
    def is_authenticated(self):
        return True


class KeycloakAuthentication(BaseAuthentication):
    """
    Custom authentication class based on Keycloak
    """

    def authenticate(self, request):
        token = self.__get_token(request)

        try:
            claims = jwt.get_unverified_claims(token)
            aud = claims["aud"]
            _kc = kc[aud]
            _kc.validate_audience(token, client_id_list=valid_clients)
            _kc.validate_authorized_party(token, client_id_list=valid_clients)
            claims = _kc.decode_token(token)

            # Api access token fails to retrieve user_info (since the token is not linked to a real user)
            # Since this authorization class checks for:
            # 1. user tokens from confidential client (pure or exchanged from public client)
            # 2. api access token
            # We can't always retrieve the user_info (only when dealing with user tokens)

            api_tokens_subs = [f"service-account-{cid}" for cid in api_clients]
            if claims["sub"] in api_tokens_subs:
                user_info = {"name": claims["sub"], "auth_flow": "api access token", "claims": "claims"}
            else:
                # Every time you call user_info you hit the auth-server userinfo endpoint
                #
                # Since this custom authentication class runs the `authenticate` method
                # every time the api receives a request in the protected route when dealing with multiple users
                # we are basically doing a ddos in the auth-server
                #
                # Since right now we are not using any user_info in the backend (probably never will)
                # i'm going to stub the user_info using decoded token claims

                # user_info = kc.user_info(token)
                user_info = {"name": claims["sub"], "auth_flow": "confidential access token", "claims": claims}
        except Exception:
            raise AuthenticationFailed()

        return (KeycloakUser(user_info=user_info), None)

    @staticmethod
    def __get_token(request):
        token = request.headers.get("Authorization")
        if not token:
            raise AuthenticationFailed()
        try:
            return token.split("Bearer ")[-1]
        except AttributeError:
            raise AuthenticationFailed()


class KeycloakApiUser(AnonymousUser):
    """
    Django Rest Framework needs an user to consider authenticated
    """

    def __init__(self, token):
        super().__init__()
        self.token = token

    @property
    def is_authenticated(self):
        return True


class KeycloakApiTokenAuthentication(BaseAuthentication):
    """
    Custom authentication class based on Keycloak
    """

    def authenticate(self, request):
        api_key = self.__get_api_key(request)

        if api_key not in settings.KEYCLOAK_API_CLIENTS.keys():
            raise AuthenticationFailed()

        api_kc = Keycloak(
            skip_pk=True,
            server_url=settings.KEYCLOAK_SERVER_URL,
            client_id=settings.KEYCLOAK_API_CLIENTS[api_key],
            client_secret_key=api_key,
            realm_name=settings.KEYCLOAK_REALM,
        )

        try:
            token = api_kc.issue_api_token()
        except Exception:
            raise AuthenticationFailed()

        return (KeycloakApiUser(token=token), None)

    @staticmethod
    def __get_api_key(request):
        token = request.headers.get("X-API-KEY")
        if not token:
            raise AuthenticationFailed()
        return token
