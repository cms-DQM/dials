from cern_auth.routers import router as cern_auth_router
from django.urls import include, path
from django.views.generic import TemplateView
from dqmio_etl.routers import router as dqmio_etl_router
from dqmio_file_indexer.routers import router as dqmio_file_indexer_router
from rest_framework import routers


router = routers.DefaultRouter()
router.registry.extend(dqmio_file_indexer_router.registry)
router.registry.extend(dqmio_etl_router.registry)
router.registry.extend(cern_auth_router.registry)

swagger_view = TemplateView.as_view(template_name="swagger-ui.html", extra_context={"schema_url": "openapi-schema"})

urlpatterns = [
    path(r"api/v1/", include(router.urls), name="api-v1"),
    path(r"api/v1/swagger", swagger_view, name="swagger-ui"),
    path(r"", swagger_view, name="swagger-ui"),
]
