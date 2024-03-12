from typing import Any

from rest_framework import exceptions, status


class KeycloakClientError(Exception):
    pass


class DetailDictMixin:
    default_detail: str
    default_code: str

    def __init__(
        self,
        detail: dict[str, Any] | str | None = None,
        code: str | None = None,
    ) -> None:
        """
        Builds a detail dictionary for the error to give more information to API users.
        """
        detail_dict = {"detail": self.default_detail, "code": self.default_code}

        if isinstance(detail, dict):
            detail_dict.update(detail)
        elif detail is not None:
            detail_dict["detail"] = detail

        if code is not None:
            detail_dict["code"] = code

        super().__init__(detail_dict)  # type: ignore


class AuthenticationFailed(DetailDictMixin, exceptions.AuthenticationFailed):
    pass


class InvalidClient(AuthenticationFailed):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Client not allowed"
    default_code = "client_not_valid"


class InvalidToken(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Token is invalid or expired"
    default_code = "token_not_valid"
