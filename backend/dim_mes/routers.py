from rest_framework import routers

from .viewsets import MEsViewSet


router = routers.SimpleRouter()
router.register(r"mes", MEsViewSet, basename="mes")
