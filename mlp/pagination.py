"""
Custom pagination function to return relative links
"""
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MLPlaygroundAPIPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        nl = self.get_next_link()
        pl = self.get_previous_link()

        return Response(
            OrderedDict({
                'next':
                nl[nl.find("/api"):] if nl is not None else None,
                'previous':
                pl[pl.find("/api"):] if pl is not None else None,

                # 'current_page':
                # int(self.request.query_params.get('page', 1)),
                'total':
                self.page.paginator.count,
                'per_page':
                self.page_size,
                'total_pages':
                round(self.page.paginator.count / self.page_size, 1),
                'results':
                data,
            }))
