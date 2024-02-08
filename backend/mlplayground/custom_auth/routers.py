from rest_framework import routers

from .viewsets import KeycloakApiTokenViewSet, KeycloakExchangeViewSet

router = routers.SimpleRouter()
router.register(r"exchange-token", KeycloakExchangeViewSet, basename="exchange-token")
router.register(r"issue-api-token", KeycloakApiTokenViewSet, basename="issue-api-token")
