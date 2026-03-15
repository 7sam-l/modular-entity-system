"""
Core views — system-level endpoints.
"""

import time

from django.db import connection
from django.db.utils import OperationalError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    GET /api/health/

    Lightweight endpoint for load balancers, uptime monitors, and CI pipelines.
    Checks that the application process is alive and the DB is reachable.
    Returns HTTP 200 on success, HTTP 503 if the DB is unreachable.
    """

    # Exclude from authentication / throttling
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    @swagger_auto_schema(
        operation_summary='Health Check',
        operation_description=(
            'Returns the health status of the API server and its database connection. '
            'Use this endpoint for load-balancer health probes.'
        ),
        responses={
            200: openapi.Response(
                description='Service healthy',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, example='healthy'),
                        'database': openapi.Schema(type=openapi.TYPE_STRING, example='ok'),
                        'response_time_ms': openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
            ),
            503: openapi.Response(description='Service unhealthy — database unreachable'),
        },
        tags=['System'],
    )
    def get(self, request: Request) -> Response:
        start = time.monotonic()

        # Probe the database with a minimal query
        db_status = 'ok'
        try:
            connection.ensure_connection()
        except OperationalError:
            db_status = 'unreachable'

        elapsed_ms = round((time.monotonic() - start) * 1000, 2)

        if db_status != 'ok':
            return Response(
                {'status': 'unhealthy', 'database': db_status, 'response_time_ms': elapsed_ms},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {'status': 'healthy', 'database': db_status, 'response_time_ms': elapsed_ms},
            status=status.HTTP_200_OK,
        )
