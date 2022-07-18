from rest_framework import routers
from data_taking_certification.api.viewsets import (
    RunCertificationViewSet,
    LumisectionCertificationViewSet,
)

router = routers.SimpleRouter()
router.register(r"run_certifications", RunCertificationViewSet)
router.register(r"lumisection_certifications", LumisectionCertificationViewSet)
