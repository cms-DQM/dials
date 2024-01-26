from rest_framework import routers

from .viewsets import (
    DQMIORunViewSet,
    DQMIOLumisectionViewSet,
    DQMIOLumisectionHistogram1DViewSet,
    DQMIOLumisectionHistogram2DViewSet
)


router = routers.SimpleRouter()
router.register(
    r"run", DQMIORunViewSet, basename="run"
)
router.register(
    r"lumisection", DQMIOLumisectionViewSet, basename="lumisection"
)
router.register(
    r"lumisectionHistogram1D", DQMIOLumisectionHistogram1DViewSet, basename="lumisectionHistogram1D"
)
router.register(
    r"lumisectionHistogram2D", DQMIOLumisectionHistogram2DViewSet, basename="lumisectionHistogram2D"
)
