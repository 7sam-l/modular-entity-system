"""
Tests for /api/vendor-product-mappings/ — CRUD and all validation rules.
"""
import pytest

URL_LIST = '/api/vendor-product-mappings/'


def detail_url(pk):
    return f'/api/vendor-product-mappings/{pk}/'


# ─── List ──────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_list_mappings_empty(api_client):
    r = api_client.get(URL_LIST)
    assert r.status_code == 200
    body = r.json()
    assert body['success'] is True
    assert body['data']['count'] == 0


@pytest.mark.django_db
def test_list_mappings_returns_existing(api_client, vendor_product_mapping):
    r = api_client.get(URL_LIST)
    assert r.json()['data']['count'] == 1


@pytest.mark.django_db
def test_list_filter_by_vendor_id(api_client, vendor_product_mapping, vendor):
    r = api_client.get(URL_LIST + f'?vendor_id={vendor.pk}')
    assert r.json()['data']['count'] == 1

    r2 = api_client.get(URL_LIST + '?vendor_id=99999')
    assert r2.json()['data']['count'] == 0


@pytest.mark.django_db
def test_list_filter_by_product_id(api_client, vendor_product_mapping, product):
    r = api_client.get(URL_LIST + f'?product_id={product.pk}')
    assert r.json()['data']['count'] == 1


@pytest.mark.django_db
def test_list_filter_primary_mapping(api_client, vendor_product_mapping):
    r = api_client.get(URL_LIST + '?primary_mapping=true')
    assert r.json()['data']['count'] == 1

    r2 = api_client.get(URL_LIST + '?primary_mapping=false')
    assert r2.json()['data']['count'] == 0


@pytest.mark.django_db
def test_list_filter_is_active(api_client, vendor_product_mapping):
    vendor_product_mapping.soft_delete()
    r = api_client.get(URL_LIST + '?is_active=true')
    assert r.json()['data']['count'] == 0

    r2 = api_client.get(URL_LIST + '?is_active=false')
    assert r2.json()['data']['count'] == 1


# ─── Create ────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_create_mapping_success(api_client, vendor, product):
    r = api_client.post(
        URL_LIST,
        {'vendor': vendor.pk, 'product': product.pk, 'primary_mapping': True},
        format='json',
    )
    assert r.status_code == 201
    body = r.json()
    assert body['success'] is True
    assert body['data']['vendor'] == vendor.pk
    assert body['data']['product'] == product.pk
    assert body['data']['primary_mapping'] is True
    # Nested detail should be present
    assert body['data']['vendor_detail']['code'] == vendor.code
    assert body['data']['product_detail']['code'] == product.code


@pytest.mark.django_db
def test_create_mapping_without_primary(api_client, vendor, product):
    r = api_client.post(
        URL_LIST,
        {'vendor': vendor.pk, 'product': product.pk},
        format='json',
    )
    assert r.status_code == 201
    assert r.json()['data']['primary_mapping'] is False


@pytest.mark.django_db
def test_create_duplicate_mapping_fails(api_client, vendor_product_mapping, vendor, product):
    r = api_client.post(
        URL_LIST,
        {'vendor': vendor.pk, 'product': product.pk},
        format='json',
    )
    assert r.status_code == 400
    assert r.json()['success'] is False
    assert 'already exists' in str(r.json())


@pytest.mark.django_db
def test_create_second_primary_mapping_fails(api_client, vendor_product_mapping, vendor, db):
    """Only one primary_mapping=True per vendor is allowed."""
    from product.models import Product
    product2 = Product.objects.create(name='Product 2', code='PROD-002')
    r = api_client.post(
        URL_LIST,
        {'vendor': vendor.pk, 'product': product2.pk, 'primary_mapping': True},
        format='json',
    )
    assert r.status_code == 400
    assert 'primary' in str(r.json()).lower()


@pytest.mark.django_db
def test_create_two_non_primary_mappings_for_same_vendor(api_client, vendor, product, db):
    """Multiple non-primary mappings for the same vendor are allowed."""
    from product.models import Product
    product2 = Product.objects.create(name='Product 2', code='PROD-002')
    r1 = api_client.post(URL_LIST, {'vendor': vendor.pk, 'product': product.pk}, format='json')
    r2 = api_client.post(URL_LIST, {'vendor': vendor.pk, 'product': product2.pk}, format='json')
    assert r1.status_code == 201
    assert r2.status_code == 201


@pytest.mark.django_db
def test_create_mapping_inactive_vendor_fails(api_client, vendor, product):
    vendor.soft_delete()
    r = api_client.post(
        URL_LIST,
        {'vendor': vendor.pk, 'product': product.pk},
        format='json',
    )
    assert r.status_code == 400


@pytest.mark.django_db
def test_create_mapping_inactive_product_fails(api_client, vendor, product):
    product.soft_delete()
    r = api_client.post(
        URL_LIST,
        {'vendor': vendor.pk, 'product': product.pk},
        format='json',
    )
    assert r.status_code == 400


@pytest.mark.django_db
def test_create_mapping_missing_vendor_fails(api_client, product):
    r = api_client.post(URL_LIST, {'product': product.pk}, format='json')
    assert r.status_code == 400


@pytest.mark.django_db
def test_create_mapping_nonexistent_vendor_fails(api_client, product):
    r = api_client.post(URL_LIST, {'vendor': 99999, 'product': product.pk}, format='json')
    assert r.status_code == 400


# ─── Retrieve ─────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_retrieve_mapping_success(api_client, vendor_product_mapping):
    r = api_client.get(detail_url(vendor_product_mapping.pk))
    assert r.status_code == 200
    assert r.json()['data']['id'] == vendor_product_mapping.pk


@pytest.mark.django_db
def test_retrieve_mapping_not_found(api_client):
    r = api_client.get(detail_url(99999))
    assert r.status_code == 404


# ─── Update ───────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_patch_mapping_deactivate(api_client, vendor_product_mapping):
    r = api_client.patch(
        detail_url(vendor_product_mapping.pk),
        {'is_active': False},
        format='json',
    )
    assert r.status_code == 200
    assert r.json()['data']['is_active'] is False


@pytest.mark.django_db
def test_patch_unset_primary_mapping(api_client, vendor_product_mapping):
    r = api_client.patch(
        detail_url(vendor_product_mapping.pk),
        {'primary_mapping': False},
        format='json',
    )
    assert r.status_code == 200
    assert r.json()['data']['primary_mapping'] is False


# ─── Soft delete ──────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_delete_mapping_soft_deletes(api_client, vendor_product_mapping):
    r = api_client.delete(detail_url(vendor_product_mapping.pk))
    assert r.status_code == 204
    vendor_product_mapping.refresh_from_db()
    assert vendor_product_mapping.is_active is False


@pytest.mark.django_db
def test_delete_mapping_not_found(api_client):
    r = api_client.delete(detail_url(99999))
    assert r.status_code == 404
