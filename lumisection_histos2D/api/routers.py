from rest_framework import routers
from lumisection_histos2D.api.viewsets import LumisectionHisto2DViewset

router = routers.SimpleRouter()
router.register(r'lumisection_histos2D', LumisectionHisto2DViewset)
