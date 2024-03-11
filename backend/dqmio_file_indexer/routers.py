from rest_framework import routers

from .viewsets import BadFileIndexViewSet, FileIndexViewSet

router = routers.SimpleRouter()
router.register(r"file-index", FileIndexViewSet, basename="file-index")
router.register(r"bad-file-index", BadFileIndexViewSet, basename="bad-file-index")
