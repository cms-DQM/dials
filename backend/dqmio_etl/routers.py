from rest_framework import routers

from .viewsets import (
    LumisectionHistogram1DMEsViewSet,
    LumisectionHistogram1DViewSet,
    LumisectionHistogram2DMEsViewSet,
    LumisectionHistogram2DViewSet,
    LumisectionViewSet,
    RunViewSet,
)


router = routers.SimpleRouter()
router.register(r"run", RunViewSet, basename="run")
router.register(r"lumisection", LumisectionViewSet, basename="lumisection")
router.register(r"lumisection-h1d-mes", LumisectionHistogram1DMEsViewSet, basename="lumisection-h1d-mes")
router.register(r"lumisection-h1d", LumisectionHistogram1DViewSet, basename="lumisection-h1d")
router.register(r"lumisection-h2d-mes", LumisectionHistogram2DMEsViewSet, basename="lumisection-h2d-mes")
router.register(r"lumisection-h2d", LumisectionHistogram2DViewSet, basename="lumisection-h2d")
