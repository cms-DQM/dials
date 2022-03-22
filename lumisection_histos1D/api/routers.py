from rest_framework import routers
from lumisection_histos1D.api.viewsets import LumisectionHisto1DViewset

router = routers.SimpleRouter()
router.register(r'lumisection_histos1D', LumisectionHisto1DViewset)
