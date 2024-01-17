from rest_framework import routers

from .viewsets import FileIndexViewSet


router = routers.SimpleRouter()
router.register(
    r"fileIndex", FileIndexViewSet, basename="fileIndex"
)
