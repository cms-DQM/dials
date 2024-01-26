from rest_framework import routers

from .viewsets import (
    RunViewSet,
    LumisectionViewSet,
    LumisectionHistogram1DViewSet,
    LumisectionHistogram2DViewSet
)


router = routers.SimpleRouter()
router.register(
    r"run", RunViewSet, basename="run"
)
router.register(
    r"lumisection", LumisectionViewSet, basename="lumisection"
)
router.register(
    r"lumisectionHistogram1D", LumisectionHistogram1DViewSet, basename="lumisectionHistogram1D"
)
router.register(
    r"lumisectionHistogram2D", LumisectionHistogram2DViewSet, basename="lumisectionHistogram2D"
)
