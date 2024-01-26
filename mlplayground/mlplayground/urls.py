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
    path("api/", include((router.urls, "api"), namespace="api"), name="api"),

    # OpenAPI 3 documentation with Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]

