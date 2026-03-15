"""
Tests for /api/vendors/ — full CRUD and validation.
"""
import pytest

URL_LIST = '/api/vendors/'


def detail_url(pk):
    return f'/api/vendors/{pk}/'


# ─── List ──────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_list_vendors_empty(api_client):
    r = api_client.get(URL_LIST)
    assert r.status_code == 200
    body = r.json()
    assert body['success'] is True
    assert body['data']['count'] == 0
    assert body['data']['results'] == []


@pytest.mark.django_db
def test_list_vendors_returns_all(api_client, vendor):
    r = api_client.get(URL_LIST)
    assert r.status_code == 200
    assert r.json()['data']['count'] == 1


@pytest.mark.django_db
def test_list_vendors_filter_active(api_client, vendor):
    vendor.soft_delete()
    r = api_client.get(URL_LIST + '?is_active=true')
    assert r.json()['data']['count'] == 0

    r2 = api_client.get(URL_LIST + '?is_active=false')
    assert r2.json()['data']['count'] == 1


# ─── Create ────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_create_vendor_success(api_client):
    payload = {'name': 'Test Vendor', 'code': 'TV-001', 'description': 'Desc'}
    r = api_client.post(URL_LIST, payload, format='json')
    assert r.status_code == 201
    body = r.json()
    assert body['success'] is True
    assert body['data']['code'] == 'TV-001'


@pytest.mark.django_db
def test_create_vendor_code_auto_uppercased(api_client):
    r = api_client.post(URL_LIST, {'name': 'Vendor', 'code': 'lower-code'}, format='json')
    assert r.status_code == 201
    assert r.json()['data']['code'] == 'LOWER-CODE'


@pytest.mark.django_db
def test_create_vendor_duplicate_code_fails(api_client, vendor):
    r = api_client.post(URL_LIST, {'name': 'Another', 'code': 'ACME'}, format='json')
    assert r.status_code == 400
    assert r.json()['success'] is False


@pytest.mark.django_db
def test_create_vendor_missing_name_fails(api_client):
    r = api_client.post(URL_LIST, {'code': 'CODE'}, format='json')
    assert r.status_code == 400
    assert 'errors' in r.json()


@pytest.mark.django_db
def test_create_vendor_missing_code_fails(api_client):
    r = api_client.post(URL_LIST, {'name': 'No Code'}, format='json')
    assert r.status_code == 400


# ─── Retrieve ─────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_retrieve_vendor_success(api_client, vendor):
    r = api_client.get(detail_url(vendor.pk))
    assert r.status_code == 200
    assert r.json()['data']['id'] == vendor.pk


@pytest.mark.django_db
def test_retrieve_vendor_not_found(api_client):
    r = api_client.get(detail_url(99999))
    assert r.status_code == 404
    assert r.json()['success'] is False


# ─── Update ───────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_put_vendor_success(api_client, vendor):
    r = api_client.put(
        detail_url(vendor.pk),
        {'name': 'Updated Name', 'code': 'ACME', 'description': 'New desc'},
        format='json',
    )
    assert r.status_code == 200
    assert r.json()['data']['name'] == 'Updated Name'


@pytest.mark.django_db
def test_patch_vendor_success(api_client, vendor):
    r = api_client.patch(detail_url(vendor.pk), {'name': 'Patched'}, format='json')
    assert r.status_code == 200
    assert r.json()['data']['name'] == 'Patched'


@pytest.mark.django_db
def test_patch_vendor_code_uniqueness(api_client, vendor):
    from vendor.models import Vendor
    other = Vendor.objects.create(name='Other', code='OTHER')
    r = api_client.patch(detail_url(vendor.pk), {'code': 'OTHER'}, format='json')
    assert r.status_code == 400


# ─── Soft delete ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_delete_vendor_soft_deletes(api_client, vendor):
    r = api_client.delete(detail_url(vendor.pk))
    assert r.status_code == 204
    vendor.refresh_from_db()
    assert vendor.is_active is False


@pytest.mark.django_db
def test_delete_vendor_not_found(api_client):
    r = api_client.delete(detail_url(99999))
    assert r.status_code == 404
