"""
Tests for /api/product-course-mappings/
"""
import pytest

URL_LIST = '/api/product-course-mappings/'


def detail_url(pk):
    return f'/api/product-course-mappings/{pk}/'


@pytest.mark.django_db
def test_list_empty(api_client):
    r = api_client.get(URL_LIST)
    assert r.status_code == 200
    assert r.json()['data']['count'] == 0


@pytest.mark.django_db
def test_create_success(api_client, product, course):
    r = api_client.post(
        URL_LIST,
        {'product': product.pk, 'course': course.pk, 'primary_mapping': True},
        format='json',
    )
    assert r.status_code == 201
    body = r.json()['data']
    assert body['product'] == product.pk
    assert body['course'] == course.pk
    assert body['product_detail']['code'] == product.code
    assert body['course_detail']['code'] == course.code


@pytest.mark.django_db
def test_create_duplicate_fails(api_client, product_course_mapping, product, course):
    r = api_client.post(
        URL_LIST,
        {'product': product.pk, 'course': course.pk},
        format='json',
    )
    assert r.status_code == 400


@pytest.mark.django_db
def test_create_second_primary_fails(api_client, product_course_mapping, product, db):
    from course.models import Course
    course2 = Course.objects.create(name='Course 2', code='C-002')
    r = api_client.post(
        URL_LIST,
        {'product': product.pk, 'course': course2.pk, 'primary_mapping': True},
        format='json',
    )
    assert r.status_code == 400


@pytest.mark.django_db
def test_filter_by_product_id(api_client, product_course_mapping, product):
    r = api_client.get(URL_LIST + f'?product_id={product.pk}')
    assert r.json()['data']['count'] == 1


@pytest.mark.django_db
def test_filter_by_course_id(api_client, product_course_mapping, course):
    r = api_client.get(URL_LIST + f'?course_id={course.pk}')
    assert r.json()['data']['count'] == 1


@pytest.mark.django_db
def test_retrieve_success(api_client, product_course_mapping):
    r = api_client.get(detail_url(product_course_mapping.pk))
    assert r.status_code == 200
    assert r.json()['data']['id'] == product_course_mapping.pk


@pytest.mark.django_db
def test_retrieve_not_found(api_client):
    r = api_client.get(detail_url(99999))
    assert r.status_code == 404


@pytest.mark.django_db
def test_soft_delete(api_client, product_course_mapping):
    r = api_client.delete(detail_url(product_course_mapping.pk))
    assert r.status_code == 204
    product_course_mapping.refresh_from_db()
    assert product_course_mapping.is_active is False


@pytest.mark.django_db
def test_inactive_product_blocked(api_client, product, course):
    product.soft_delete()
    r = api_client.post(
        URL_LIST,
        {'product': product.pk, 'course': course.pk},
        format='json',
    )
    assert r.status_code == 400


@pytest.mark.django_db
def test_inactive_course_blocked(api_client, product, course):
    course.soft_delete()
    r = api_client.post(
        URL_LIST,
        {'product': product.pk, 'course': course.pk},
        format='json',
    )
    assert r.status_code == 400
