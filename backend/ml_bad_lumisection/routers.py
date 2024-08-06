from rest_framework import routers

from .viewsets import MLBadLumisectionViewSet


router = routers.SimpleRouter()
router.register(r"ml-bad-lumisection", MLBadLumisectionViewSet, basename="ml-bad-lumisection")
