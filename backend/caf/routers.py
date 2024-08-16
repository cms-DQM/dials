from rest_framework import routers

from .viewsets import CAFViewSet


router = routers.SimpleRouter()
router.register(r"caf", CAFViewSet, basename="caf")
