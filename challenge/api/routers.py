from rest_framework import routers
from challenge.api.viewsets import TaskViewSet

router = routers.SimpleRouter()
router.register(r'tasks', TaskViewSet)
