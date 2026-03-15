"""
Tests for Product, Course, and Certification master endpoints.
These mirror the Vendor tests but cover the cross-entity filtering.
"""
import pytest


# ─── Products ─────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_list_products_empty(api_client):
    r = api_client.get('/api/products/')
    assert r.status_code == 200
    assert r.json()['data']['count'] == 0


@pytest.mark.django_db
def test_create_product(api_client):
    r = api_client.post('/api/products/', {'name': 'My Product', 'code': 'PROD-X'}, format='json')
    assert r.status_code == 201
    assert r.json()['data']['code'] == 'PROD-X'


@pytest.mark.django_db
def test_product_filter_by_vendor_id(api_client, vendor_product_mapping, vendor):
    r = api_client.get(f'/api/products/?vendor_id={vendor.pk}')
    assert r.json()['data']['count'] == 1


@pytest.mark.django_db
def test_product_filter_vendor_no_results(api_client, vendor):
    r = api_client.get(f'/api/products/?vendor_id={vendor.pk}')
    assert r.json()['data']['count'] == 0


@pytest.mark.django_db
def test_product_duplicate_code_fails(api_client, product):
    r = api_client.post('/api/products/', {'name': 'Dup', 'code': product.code}, format='json')
    assert r.status_code == 400


@pytest.mark.django_db
def test_product_soft_delete(api_client, product):
    r = api_client.delete(f'/api/products/{product.pk}/')
    assert r.status_code == 204
    product.refresh_from_db()
    assert product.is_active is False


# ─── Courses ──────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_list_courses_empty(api_client):
    r = api_client.get('/api/courses/')
    assert r.status_code == 200
    assert r.json()['data']['count'] == 0


@pytest.mark.django_db
def test_create_course(api_client):
    r = api_client.post(
        '/api/courses/',
        {'name': 'My Course', 'code': 'CRSE-X', 'description': 'A course'},
        format='json',
    )
    assert r.status_code == 201
    assert r.json()['data']['code'] == 'CRSE-X'


@pytest.mark.django_db
def test_course_filter_by_product_id(api_client, product_course_mapping, product):
    r = api_client.get(f'/api/courses/?product_id={product.pk}')
    assert r.json()['data']['count'] == 1


@pytest.mark.django_db
def test_course_soft_delete(api_client, course):
    r = api_client.delete(f'/api/courses/{course.pk}/')
    assert r.status_code == 204
    course.refresh_from_db()
    assert course.is_active is False


# ─── Certifications ────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_list_certifications_empty(api_client):
    r = api_client.get('/api/certifications/')
    assert r.status_code == 200
    assert r.json()['data']['count'] == 0


@pytest.mark.django_db
def test_create_certification(api_client):
    r = api_client.post(
        '/api/certifications/',
        {'name': 'My Cert', 'code': 'CERT-X'},
        format='json',
    )
    assert r.status_code == 201
    assert r.json()['data']['code'] == 'CERT-X'


@pytest.mark.django_db
def test_certification_filter_by_course_id(api_client, course_certification_mapping, course):
    r = api_client.get(f'/api/certifications/?course_id={course.pk}')
    assert r.json()['data']['count'] == 1


@pytest.mark.django_db
def test_certification_soft_delete(api_client, certification):
    r = api_client.delete(f'/api/certifications/{certification.pk}/')
    assert r.status_code == 204
    certification.refresh_from_db()
    assert certification.is_active is False


@pytest.mark.django_db
def test_retrieve_certification_not_found(api_client):
    r = api_client.get('/api/certifications/99999/')
    assert r.status_code == 404
    assert r.json()['success'] is False


# ─── Pagination ───────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_list_pagination_structure(api_client, vendor):
    r = api_client.get('/api/vendors/')
    data = r.json()['data']
    assert 'count' in data
    assert 'total_pages' in data
    assert 'current_page' in data
    assert 'next' in data
    assert 'previous' in data
    assert 'results' in data


@pytest.mark.django_db
def test_page_size_param(api_client, db):
    from vendor.models import Vendor
    for i in range(5):
        Vendor.objects.create(name=f'V{i}', code=f'CODE-{i}')
    r = api_client.get('/api/vendors/?page_size=2')
    data = r.json()['data']
    assert len(data['results']) == 2
    assert data['count'] == 5
    assert data['total_pages'] == 3
