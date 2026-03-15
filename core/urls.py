"""
Core utility endpoints.

GET /api/health/   — lightweight health check for load balancers / monitoring
"""

from django.urls import path
from .views import HealthCheckView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
