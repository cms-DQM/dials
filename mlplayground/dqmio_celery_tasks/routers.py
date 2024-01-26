from rest_framework import routers

from .viewsets import CeleryTasksViewSet


router = routers.SimpleRouter()
router.register(
    r"celeryTasks", CeleryTasksViewSet, basename="celeryTasks"
)
