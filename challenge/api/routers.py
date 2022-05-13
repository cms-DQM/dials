from rest_framework import routers
from challenge.api.viewsets import TaskViewSet, StrategyViewSet, PredictionViewSet

router = routers.SimpleRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"strategies", StrategyViewSet)
router.register(r"predictions", PredictionViewSet)
