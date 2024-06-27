from cern_auth.routers import router as cern_auth_router
from dataset_index.routers import router as dataset_index_router
from dim_mes.routers import router as dim_mes_router
from django.urls import include, path
from django.views.generic import TemplateView
from file_index.routers import router as file_index_router
from lumisection.routers import router as lumisection_router
from ml_models_index.routers import router as ml_models_index_router
from rest_framework import routers
from run.routers import router as run_router
from th1.routers import router as th1_router
from th2.routers import router as th2_router


router = routers.DefaultRouter()
router.registry.extend(dataset_index_router.registry)
router.registry.extend(file_index_router.registry)
router.registry.extend(dim_mes_router.registry)
router.registry.extend(run_router.registry)
router.registry.extend(lumisection_router.registry)
router.registry.extend(th1_router.registry)
router.registry.extend(th2_router.registry)
router.registry.extend(ml_models_index_router.registry)
router.registry.extend(cern_auth_router.registry)

swagger_view = TemplateView.as_view(template_name="swagger-ui.html", extra_context={"schema_url": "openapi-schema"})

urlpatterns = [
    path(r"api/v1/", include(router.urls), name="api-v1"),
    path(r"api/v1/swagger", swagger_view, name="swagger-ui"),
    path(r"", swagger_view, name="swagger-ui"),
]
