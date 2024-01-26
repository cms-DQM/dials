from rest_framework import routers

from .viewsets import FileIndexViewSet


router = routers.SimpleRouter()
router.register(r"file-index", FileIndexViewSet, basename="file-index")
