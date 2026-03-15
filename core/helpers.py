"""
Shared response helpers used by every view in the project.
"""

import logging
from typing import Any, TypeVar

from django.db.models import Model
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger('app')

M = TypeVar('M', bound=Model)


def get_object_or_error(model: type, pk: Any):
    """
    Fetch model.objects.get(pk=pk) and return a clean 404 on failure.
    Returns (instance, None) on success, (None, Response) on failure.
    """
    try:
        return model.objects.get(pk=pk), None
    except model.DoesNotExist:
        logger.debug('%s pk=%s not found.', model.__name__, pk)
        return None, error_response(
            message=f'{model.__name__} with id {pk} not found.',
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except (ValueError, TypeError):
        return None, error_response(
            message=f'Invalid id "{pk}". Must be a positive integer.',
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def success_response(data: Any, message: str = 'Success.', status_code: int = status.HTTP_200_OK) -> Response:
    """Standard 2xx envelope."""
    return Response({'success': True, 'message': message, 'data': data}, status=status_code)


def created_response(data: Any, message: str) -> Response:
    return success_response(data, message=message, status_code=status.HTTP_201_CREATED)


def no_content_response(message: str) -> Response:
    return success_response(data=None, message=message, status_code=status.HTTP_204_NO_CONTENT)


def error_response(message: str = 'An error occurred.', errors: Any = None,
                   status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
    """Standard error envelope."""
    body = {'success': False, 'message': message, 'data': None}
    if errors is not None:
        body['errors'] = errors
    return Response(body, status=status_code)


def validation_error_response(entity: str, errors: Any) -> Response:
    return error_response(
        message=f'{entity} validation failed.',
        errors=errors,
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def parse_int_param(request, param: str):
    """
    Parse a query param that must be a positive integer.
    Returns (value, None) | (None, None) | (None, error_response).
    """
    raw = request.query_params.get(param)
    if raw is None:
        return None, None
    try:
        val = int(raw)
        if val <= 0:
            raise ValueError
        return val, None
    except (ValueError, TypeError):
        return None, error_response(message=f'Query param "{param}" must be a positive integer.')
