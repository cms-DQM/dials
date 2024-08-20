from rest_framework import routers

from .viewsets import RunRegistryViewSet


router = routers.SimpleRouter()
router.register(r"runregistry", RunRegistryViewSet, basename="runregistry")
