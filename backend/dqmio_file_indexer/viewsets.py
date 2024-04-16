import logging
from typing import ClassVar

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.authentication import BaseAuthentication
from utils.db_router import GenericViewSetRouter
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakClientSecretAuthentication,
    CERNKeycloakConfidentialAuthentication,
)

from .filters import FileIndexFilter
from .models import FileIndex
from .serializers import FileIndexSerializer


logger = logging.getLogger(__name__)


@method_decorator(cache_page(settings.CACHE_TTL), name="retrieve")
@method_decorator(cache_page(settings.CACHE_TTL), name="list")
@method_decorator(vary_on_headers(settings.WORKSPACE_HEADER), name="retrieve")
@method_decorator(vary_on_headers(settings.WORKSPACE_HEADER), name="list")
class FileIndexViewSet(GenericViewSetRouter, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = FileIndex.objects.all().order_by("file_id")
    serializer_class = FileIndexSerializer
    filterset_class = FileIndexFilter
    filter_backends: ClassVar[list[DjangoFilterBackend]] = [DjangoFilterBackend]
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]
