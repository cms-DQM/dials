from django.utils.functional import cached_property

from .token import CERNKeycloakToken


class CERNKeycloakUser:
    """
    A dummy user class modeled after django.contrib.auth.models.AnonymousUser.
    Used in conjunction with the `KeycloakAuthentication` backend to
    implement single sign-on functionality.
    """

    is_active = True

    def __init__(self, token: CERNKeycloakToken) -> None:
        super().__init__()
        self.token = token

    def __str__(self) -> str:
        return f"CERNKeycloakUser <{self.username}>"

    @cached_property
    def username(self) -> str:
        return self.token.claims["sub"]

    @cached_property
    def cern_roles(self) -> list:
        return self.token.claims["cern_roles"]

    @cached_property
    def resource_roles(self) -> list:
        return self.token.claims["resource_access"][self.token.aud]["roles"]

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def is_authenticated(self) -> True:
        return self.is_authenticated
