from rest_framework import routers

from .viewsets import (
    RunViewSet,
    LumisectionViewSet,
    LumisectionHistogram1DViewSet,
    LumisectionHistogram2DViewSet
)


router = routers.SimpleRouter()
router.register(r"run", RunViewSet, basename="run")
router.register(r"lumisection", LumisectionViewSet, basename="lumisection")
router.register(r"lumisection-h1d", LumisectionHistogram1DViewSet, basename="lumisection-h1d")
router.register(r"lumisection-h2d", LumisectionHistogram2DViewSet, basename="lumisection-h2d")
