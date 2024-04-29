from rest_framework.pagination import CursorPagination


class EndlessPagination(CursorPagination):
    cursor_query_param = "next_token"
    ordering_param = "order_by"

    def get_ordering(self, request, queryset, view):
        default_order_by = list(queryset.query.order_by)
        if self.ordering_param in request.query_params:
            return request.query_params.getlist(self.ordering_param, None)
        return default_order_by
