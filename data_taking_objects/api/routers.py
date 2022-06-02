from rest_framework import routers
from data_taking_objects.api.viewsets import RunViewSet, LumisectionViewSet

router = routers.SimpleRouter()
router.register(r"runs", RunViewSet)
router.register(r"lumisections", LumisectionViewSet)
