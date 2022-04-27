from django.urls import path
from data_taking_certification.views import (
    run_certification_view,
    lumisection_certification_view,
)

app_name = "data_taking_certification"

urlpatterns = [
    path("run_certification/", run_certification_view, name="run-certification-view"),
    path(
        "lumisection_certification/",
        lumisection_certification_view,
        name="lumisection-certification-view",
    ),
]
