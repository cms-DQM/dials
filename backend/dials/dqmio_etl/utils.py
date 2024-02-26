from functools import wraps

from django.db.models import Func
from rest_framework.exceptions import NotFound
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


class SplitPart(Func):
    function = "split_part"
    arity = 3
