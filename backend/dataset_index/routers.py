from rest_framework import routers

from .viewsets import DatasetIndexViewSet


router = routers.SimpleRouter()
router.register(r"dataset-index", DatasetIndexViewSet, basename="dataset-index")
