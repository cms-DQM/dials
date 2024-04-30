from rest_framework import routers

from .viewsets import RunViewSet


router = routers.SimpleRouter()
router.register(r"run", RunViewSet, basename="run")
