from rest_framework import routers

from .viewsets import LumisectionViewSet


router = routers.SimpleRouter()
router.register(r"lumisection", LumisectionViewSet, basename="lumisection")
