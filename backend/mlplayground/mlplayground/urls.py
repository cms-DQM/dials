from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from dqmio_file_indexer.routers import router as dqmio_file_indexer_router
from dqmio_etl.routers import router as dqmio_etl_router
from dqmio_celery_tasks.routers import router as dqmio_celery_tasks_router

router = routers.DefaultRouter()
router.registry.extend(dqmio_file_indexer_router.registry)
router.registry.extend(dqmio_etl_router.registry)
router.registry.extend(dqmio_celery_tasks_router.registry)

urlpatterns = [
    path(r"api/v1/", include(router.urls), name="api-v1"),
    path(r"api/v1/schema", SpectacularAPIView.as_view(), name="schema-v1"),
    path(r"api/v1/swagger", SpectacularSwaggerView.as_view(url_name="schema-v1"), name="swagger-v1")
]
