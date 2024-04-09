import traceback
from functools import wraps

from django.core.paginator import Paginator
from django.db import OperationalError, connection, transaction
from django.utils.functional import cached_property
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def paginate(page_size, serializer_class):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            res_size = len(response)

            page = int(request.request.GET.get("page", 1))
            current_url = request.request.build_absolute_uri().split("?")[0]
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            paginated_data = response[start_index:end_index]

            if len(paginated_data) == 0:
                raise NotFound(detail="Invalid page.")

            next_page = None if end_index > res_size else current_url + f"?page={page+1}"
            previous_page = None if start_index == 0 else current_url + f"?page={page-1}"

            return Response(
                {
                    "count": res_size,
                    "next": next_page,
                    "previous": previous_page,
                    "results": serializer_class(paginated_data, many=True).data,
                }
            )

        return wrapper

    return decorator


class LargeTablePaginator(Paginator):
    """
    Source: https://gist.github.com/noviluni/d86adfa24843c7b8ed10c183a9df2afe
    """

    @cached_property
    def count(self):
        """
        Returns an estimated number of objects, across all pages.
        """
        timeout = 200  # ms
        try:
            with transaction.atomic(), connection.cursor() as cursor:
                cursor.execute(f"SET LOCAL statement_timeout TO {timeout};")
                return super().count
        except OperationalError:
            pass

        if not self.object_list.query.where:
            try:
                with transaction.atomic(), connection.cursor() as cursor:
                    # Obtain estimated values (only valid with PostgreSQL)
                    cursor.execute(
                        "SELECT reltuples FROM pg_class WHERE relname = %s",
                        [self.object_list.query.model._meta.db_table],
                    )
                    estimate = int(cursor.fetchone()[0])
                    return estimate
            except Exception:  # noqa: BLE001
                # If any other exception occurred fall back to default behaviour
                traceback.print_exc()
                pass

        return super().count


class LargeTablePageNumberPagination(PageNumberPagination):
    django_paginator_class = LargeTablePaginator
