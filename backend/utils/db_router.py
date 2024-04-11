from django.conf import settings
from rest_framework.exceptions import NotFound


def get_workspace_from_role(roles: list, use_default_if_not_found: bool = False) -> str | None:
    for workspace_name, workspace_role in settings.WORKSPACES.items():
        if workspace_role in roles:
            return workspace_name
    if use_default_if_not_found:
        return settings.DEFAULT_WORKSPACE
    return None


class GenericViewSetRouter:
    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = queryset.query.order_by
        queryset = queryset.model.objects
        workspace = self.request.headers.get(settings.WORKSPACE_HEADER.capitalize())

        if workspace:
            if workspace not in settings.WORKSPACES.keys():
                raise NotFound(detail=f"Workspace '{workspace}' not found", code=404)
            queryset = queryset.using(workspace)
        else:
            user_roles = self.request.user.cern_roles
            workspace = get_workspace_from_role(user_roles)
            workspace = workspace or settings.DEFAULT_WORKSPACE
            queryset = queryset.using(workspace)

        return queryset.all().order_by(*order_by)
