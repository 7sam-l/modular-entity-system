"""
Custom DRF exception handler.

Wraps ALL unhandled and DRF exceptions in our standard JSON envelope so the
API surface is consistent — the client always receives:

    {
        "success": false,
        "message": "<human-readable description>",
        "data": null,
        "errors": { ... }   # present only when field-level detail is available
    }
"""

import logging
from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    APIException,
    NotFound,
    ValidationError,
    PermissionDenied,
    NotAuthenticated,
    MethodNotAllowed,
    Throttled,
)

logger = logging.getLogger('app')


# ─── Custom application exception ──────────────────────────────────────────────

class ApplicationError(APIException):
    """
    Base class for domain-level exceptions raised anywhere in the project.
    Raise this (or a subclass) to produce a clean 400 error response.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A business-logic error occurred.'
    default_code = 'application_error'


class DuplicateMappingError(ApplicationError):
    """Raised when a duplicate (parent, child) mapping is attempted."""
    default_detail = 'This mapping already exists.'
    default_code = 'duplicate_mapping'


class PrimaryMappingConflictError(ApplicationError):
    """Raised when a second primary_mapping=True is created for the same parent."""
    default_detail = 'A primary mapping for this parent already exists.'
    default_code = 'primary_mapping_conflict'


# ─── Handler ───────────────────────────────────────────────────────────────────

def custom_exception_handler(exc: Exception, context: dict) -> Response | None:
    """
    Called by DRF whenever an exception propagates out of a view.

    1. Delegates to DRF's default handler to get the standard Response.
    2. Re-shapes the response body into our standard envelope.
    3. Logs server-side errors (5xx) at ERROR level.
    """
    # Let DRF handle the exception first (returns None for non-DRF exceptions)
    response = exception_handler(exc, context)

    if response is None:
        # Unhandled exception — log it and return a generic 500
        logger.exception(
            'Unhandled exception in view %s: %s',
            context.get('view', 'unknown'),
            exc,
        )
        return Response(
            {
                'success': False,
                'message': 'An unexpected server error occurred. Please try again later.',
                'data': None,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Build human-readable message from the exception type
    message = _build_message(exc, response)

    # Reshape body
    new_body: dict[str, Any] = {
        'success': False,
        'message': message,
        'data': None,
    }

    # Include detailed field errors for validation failures
    if isinstance(exc, ValidationError) and isinstance(response.data, (dict, list)):
        new_body['errors'] = response.data

    response.data = new_body
    return response


def _build_message(exc: Exception, response: Response) -> str:
    """Derive a clean human-readable message from an exception."""
    if isinstance(exc, NotFound):
        return 'The requested resource was not found.'
    if isinstance(exc, PermissionDenied):
        return 'You do not have permission to perform this action.'
    if isinstance(exc, NotAuthenticated):
        return 'Authentication credentials were not provided.'
    if isinstance(exc, MethodNotAllowed):
        return f'HTTP method {exc.args[0] if exc.args else ""} is not allowed on this endpoint.'
    if isinstance(exc, Throttled):
        wait = getattr(exc, 'wait', None)
        if wait:
            return f'Request was throttled. Try again in {int(wait)} seconds.'
        return 'Request was throttled. Too many requests.'
    if isinstance(exc, ValidationError):
        return 'Validation failed. Please check the errors field for details.'
    if isinstance(exc, APIException):
        # Use the exception's detail if it's a simple string
        detail = exc.detail
        if isinstance(detail, str):
            return detail
        return 'A request error occurred.'
    return 'An error occurred.'
