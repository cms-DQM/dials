from drf_spectacular.extensions import OpenApiAuthenticationExtension


class KeycloakAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "custom_auth.keycloak.KeycloakAuthentication"
    name = "KeycloakAuthentication"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "Bearer",
            "bearerFormat": "JWT",
            "in": "header",
            "name": "Authorization",
            "description": "Keycloak confidential token flow-based authentication",
        }


class KeycloakApiTokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "custom_auth.keycloak.KeycloakApiTokenAuthentication"
    name = "KeycloakApiTokenAuthentication"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY",
            "description": "Keycloak api token access-based authentication",
        }
