"""
Pagination classes used by all list endpoints.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    """
    Adds page / page_size query params to every list endpoint.

    Query params:
        ?page=1          — page number (1-indexed)
        ?page_size=20    — override the default page size (max 100)

    Response envelope:
        {
            "success": true,
            "message": "...",
            "data": {
                "count":     <total records>,
                "total_pages": <number of pages>,
                "current_page": <current page number>,
                "next":      "<url | null>",
                "previous":  "<url | null>",
                "results":   [ ... ]
            }
        }
    """

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data: list) -> Response:
        return Response(
            {
                'success': True,
                'message': 'Results retrieved successfully.',
                'data': {
                    'count': self.page.paginator.count,
                    'total_pages': self.page.paginator.num_pages,
                    'current_page': self.page.number,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'results': data,
                },
            }
        )

    def get_paginated_response_schema(self, schema: dict) -> dict:
        """Describe the paginated envelope for drf-yasg."""
        return {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'message': {'type': 'string'},
                'data': {
                    'type': 'object',
                    'properties': {
                        'count': {'type': 'integer'},
                        'total_pages': {'type': 'integer'},
                        'current_page': {'type': 'integer'},
                        'next': {'type': 'string', 'nullable': True},
                        'previous': {'type': 'string', 'nullable': True},
                        'results': schema,
                    },
                },
            },
        }
