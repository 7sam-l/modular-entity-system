"""
Shared queryset filtering helpers.

Each function accepts a QuerySet and the request, applies relevant
query-param filters, and returns the filtered QuerySet.
These are imported by individual app views to avoid copy-pasting filter logic.
"""

from django.db.models import QuerySet
from rest_framework.request import Request

from .helpers import parse_int_param, error_response


def filter_is_active(queryset: QuerySet, request: Request):
    """
    Apply ?is_active=true|false to a queryset.
    Returns (filtered_queryset, None) or (None, error_response).
    """
    raw = request.query_params.get('is_active')
    if raw is None:
        return queryset, None
    if raw.lower() not in ('true', 'false'):
        return None, error_response(
            message='Query param "is_active" must be "true" or "false".'
        )
    return queryset.filter(is_active=(raw.lower() == 'true')), None


def filter_by_int_param(queryset: QuerySet, request: Request, param: str, field: str):
    """
    Apply ?<param>=<int> as queryset.filter(<field>=<int>).
    Returns (filtered_queryset, None) or (None, error_response).
    """
    value, err = parse_int_param(request, param)
    if err:
        return None, err
    if value is not None:
        queryset = queryset.filter(**{field: value})
    return queryset, None


def filter_primary_mapping(queryset: QuerySet, request: Request):
    """Apply ?primary_mapping=true|false."""
    raw = request.query_params.get('primary_mapping')
    if raw is None:
        return queryset, None
    if raw.lower() not in ('true', 'false'):
        return None, error_response(
            message='Query param "primary_mapping" must be "true" or "false".'
        )
    return queryset.filter(primary_mapping=(raw.lower() == 'true')), None
