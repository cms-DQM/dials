from rest_framework import routers

from .viewsets import DQMIOCeleryTasksViewSet


router = routers.SimpleRouter()
router.register(
    r"celeryTasks", DQMIOCeleryTasksViewSet, basename="celeryTasks"
)
