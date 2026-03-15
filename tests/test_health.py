"""Tests for the health check endpoint."""

import pytest


@pytest.mark.django_db
def test_health_check_returns_200(api_client):
    response = api_client.get('/api/health/')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'
    assert data['database'] == 'ok'
    assert 'response_time_ms' in data
