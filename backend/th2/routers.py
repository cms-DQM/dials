from rest_framework import routers

from .viewsets import TH2ViewSet


router = routers.SimpleRouter()
router.register(r"th2", TH2ViewSet, basename="th2")
