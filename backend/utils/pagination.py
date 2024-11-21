import json
import operator
from functools import reduce

from django.db.models.query import Q
from rest_framework.pagination import CursorPagination, _reverse_ordering


class DynamicMultiOrderingCursorPagination(CursorPagination):
    """
    Django RestFramework CursorPagination "works" with multiple order_by fields,
    but when building the query it ignores all the fields and use only the first one.
    More info: https://github.com/encode/django-rest-framework/discussions/7888

    The patch applied in the CursorPagination class was inspired in this set of modification:
    https://github.com/encode/django-rest-framework/commit/9408b4311cb49519b820b0464d13cc982cbdead4#diff-9bf84726a74acdcb626ce49b9a73aeb84b9c3007034273641a8596786b25c6f3L19
    """

    cursor_query_param = "next_token"
    ordering_param = "order_by"
    page_size_query_param = "page_size"
    max_page_size = 500

    def get_ordering(self, request, queryset, view):
        default_order_by = list(queryset.query.order_by)
        if self.ordering_param in request.query_params:
            return request.query_params.getlist(self.ordering_param, None)
        return default_order_by

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request)
        if not self.page_size:
            return None

        self.base_url = request.build_absolute_uri()
        self.ordering = self.get_ordering(request, queryset, view)

        self.cursor = self.decode_cursor(request)

        if self.cursor is None:
            (offset, reverse, current_position) = (0, False, None)
        else:
            (offset, reverse, current_position) = self.cursor

        # Cursor pagination always enforces an ordering.
        if reverse:
            queryset = queryset.order_by(*_reverse_ordering(self.ordering))
        else:
            queryset = queryset.order_by(*self.ordering)

        # If we have a cursor with a fixed position then filter by that.
        if current_position is not None:
            current_position_list = json.loads(current_position)
            q_objects_equals = {}
            q_objects_compare = {}

            for order, position in zip(self.ordering, current_position_list, strict=False):
                is_reversed = order.startswith("-")
                order_attr = order.lstrip("-")

                q_objects_equals[order] = Q(**{order_attr: position})

                # Test for: (cursor reversed) XOR (queryset reversed)
                if self.cursor.reverse != is_reversed:
                    q_objects_compare[order] = Q(**{(order_attr + "__lt"): position})
                else:
                    q_objects_compare[order] = Q(**{(order_attr + "__gt"): position})

            filter_list = []
            for i in range(len(self.ordering)):
                # For this to work we filter the index by (A, B) > (X, Y)
                # The following expression in NOT THE SAME: A > X AND B > Y
                # What we must do: (A > X) OR ((A = X) AND (B > Y))
                #
                # This is true for
                # (A, B, C, ...) > (X, Y, Z, ...)
                # That turns:
                # (A > X)
                # OR ((A = X) AND (B > Y))
                # OR ((A = X) AND (B = Y) AND (C > Z))
                # OR ...
                if i == 0:
                    greater_than_q = q_objects_compare[self.ordering[0]]
                    filter_list.append(greater_than_q)
                else:
                    greater_than_q = q_objects_compare[self.ordering[i]]
                    sub_filters = [q_objects_equals[e] for e in self.ordering[:i]]
                    sub_filters.append(greater_than_q)
                    filter_list.append(reduce(operator.and_, sub_filters))

            queryset = queryset.filter(reduce(operator.or_, filter_list))

        # If we have an offset cursor then offset the entire page by that amount.
        # We also always fetch an extra item in order to determine if there is a
        # page following on from this one.
        results = list(queryset[offset : offset + self.page_size + 1])
        self.page = list(results[: self.page_size])

        # Determine the position of the final item following the page.
        if len(results) > len(self.page):
            has_following_position = True
            following_position = self._get_position_from_instance(results[-1], self.ordering)
        else:
            has_following_position = False
            following_position = None

        if reverse:
            # If we have a reverse queryset, then the query ordering was in reverse
            # so we need to reverse the items again before returning them to the user.
            self.page = list(reversed(self.page))

            # Determine next and previous positions for reverse cursors.
            self.has_next = (current_position is not None) or (offset > 0)
            self.has_previous = has_following_position
            if self.has_next:
                self.next_position = current_position
            if self.has_previous:
                self.previous_position = following_position
        else:
            # Determine next and previous positions for forward cursors.
            self.has_next = has_following_position
            self.has_previous = (current_position is not None) or (offset > 0)
            if self.has_next:
                self.next_position = following_position
            if self.has_previous:
                self.previous_position = current_position

        # Display page controls in the browsable API if there is more
        # than one page.
        if (self.has_previous or self.has_next) and self.template is not None:
            self.display_page_controls = True

        return self.page

    def _get_position_from_instance(self, instance, ordering):
        fields = []

        for o in ordering:
            field_name = o.lstrip("-")
            if isinstance(instance, dict):
                attr = instance[field_name]
            else:
                attr = getattr(instance, field_name)

            fields.append(str(attr))

        return json.dumps(fields).encode()
