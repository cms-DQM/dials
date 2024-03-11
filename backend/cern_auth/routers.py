from rest_framework import routers

from .viewsets import AuthViewSet


router = routers.SimpleRouter()
router.register(r"auth", AuthViewSet, basename="auth")
