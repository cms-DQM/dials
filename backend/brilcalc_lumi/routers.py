from rest_framework import routers

from .viewsets import BrilcalcLumiViewSet


router = routers.SimpleRouter()
router.register(r"brilcalc-lumi", BrilcalcLumiViewSet, basename="brilcalc-lumi")
