from rest_framework import routers

from .viewsets import MLModelsIndexViewSet


router = routers.SimpleRouter()
router.register(r"ml-models-index", MLModelsIndexViewSet, basename="ml-models-index")
