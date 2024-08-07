from rest_framework import routers

from .viewsets import OMSProxyViewSet


router = routers.SimpleRouter()
router.register(r"oms-proxy", OMSProxyViewSet, basename="oms-proxy")
