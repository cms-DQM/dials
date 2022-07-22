"""mlp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework import routers
from rest_framework.schemas import get_schema_view

from histogram_file_manager.api.routers import router as histogram_data_file_router
from histograms.api.routers import router as histograms_router
from challenge.api.routers import router as challenge_router
from data_taking_objects.api.routers import router as data_taking_objects_router
from data_taking_certification.api.routers import (
    router as data_taking_certification_router,
)

# Create a router and extend it will all apps' api endpoints
router = routers.DefaultRouter()
router.registry.extend(histogram_data_file_router.registry)
router.registry.extend(histograms_router.registry)
router.registry.extend(challenge_router.registry)
router.registry.extend(data_taking_objects_router.registry)
router.registry.extend(data_taking_certification_router.registry)

urlpatterns = [
    path("", include("home.urls")),
    path("listdatasets/", include("listdatasets.urls")),
    path("data_taking_objects/", include("data_taking_objects.urls")),
    path("data_taking_certification/", include("data_taking_certification.urls")),
    path("histograms/", include("histograms.urls")),
    path("challenge/", include("challenge.urls")),
    path("admin/", admin.site.urls),
    path("histogram_file_manager/", include("histogram_file_manager.urls")),
    path("api/", include((router.urls, "api"), namespace="api"), name="api"),
    path(
        "openapi",
        get_schema_view(title="MLPlayground", description="API", version="0.0.0"),
        name="openapi-schema",
    ),
    path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
    path("accounts/", include("allauth.urls")),
    # path('__debug__/', include('debug_toolbar.urls')),
]
