from rest_framework import routers

from .viewsets import TH1ViewSet


router = routers.SimpleRouter()
router.register(r"th1", TH1ViewSet, basename="th1")
