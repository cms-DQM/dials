from rest_framework import routers
from histograms.api.viewsets import RunHistogramViewSet, LumisectionHistogram1DViewSet, LumisectionHistogram2DViewSet

router = routers.SimpleRouter()
router.register(r'run_histograms', RunHistogramViewSet)
router.register(r'lumisection_histograms_1d', LumisectionHistogram1DViewSet)
router.register(r'lumisection_histograms_2d', LumisectionHistogram2DViewSet)
