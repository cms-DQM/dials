"""
DRF Header utilities

- CustomAutoSchema: Useful for adding global parameters to the schema
--------------------------------------------------------------------
We can use this class in REST_FRAMEWORK setting:
"DEFAULT_SCHEMA_CLASS": "utils.drf_header.CustomAutoSchema"
--------------------------------------------------------------------
If we wanted to have fine-grained control over each ViewSet we could do the following:

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="workspace",
                type=str,
                location=OpenApiParameter.HEADER,
                description="Workspace",
            )
        ]
    )
)
class FileIndexViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
"""

from typing import ClassVar

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import OpenApiParameter


class CustomAutoSchema(AutoSchema):
    ignore_routes: ClassVar[list[str]] = ["auth"]
    global_params: ClassVar[list[OpenApiParameter]] = [
        OpenApiParameter(
            name="workspace",
            type=str,
            location=OpenApiParameter.HEADER,
            description="Workspace",
        )
    ]

    def get_override_parameters(self):
        params = super().get_override_parameters()
        for route_name in self.ignore_routes:
            if route_name in self.path:
                return params
        return params + self.global_params
