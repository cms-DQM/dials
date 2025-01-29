from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CERNKeycloakClientSecretAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "utils.rest_framework_cern_sso.authentication.CERNKeycloakClientSecretAuthentication"
    name = "Client Secret Key"
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "X-CLIENT-SECRET",
            "description": "CERN's Keycloak api access authentication",
        }


class CERNKeycloakBearerAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "utils.rest_framework_cern_sso.authentication.CERNKeycloakBearerAuthentication"
    name = "JWT Token"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "Bearer",
            "bearerFormat": "JWT",
            "in": "header",
            "name": "Authorization",
            "description": "CERN's Keycloak bearer authentication",
        }
