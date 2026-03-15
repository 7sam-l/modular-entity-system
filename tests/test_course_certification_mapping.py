"""
Tests for /api/course-certification-mappings/
"""
import pytest

URL_LIST = '/api/course-certification-mappings/'


def detail_url(pk):
    return f'/api/course-certification-mappings/{pk}/'


@pytest.mark.django_db
def test_list_empty(api_client):
    r = api_client.get(URL_LIST)
    assert r.status_code == 200
    assert r.json()['data']['count'] == 0


@pytest.mark.django_db
def test_create_success(api_client, course, certification):
    r = api_client.post(
        URL_LIST,
        {'course': course.pk, 'certification': certification.pk, 'primary_mapping': True},
        format='json',
    )
    assert r.status_code == 201
    body = r.json()['data']
    assert body['course'] == course.pk
    assert body['certification'] == certification.pk
    assert body['course_detail']['code'] == course.code
    assert body['certification_detail']['code'] == certification.code


@pytest.mark.django_db
def test_create_duplicate_fails(api_client, course_certification_mapping, course, certification):
    r = api_client.post(
        URL_LIST,
        {'course': course.pk, 'certification': certification.pk},
        format='json',
    )
    assert r.status_code == 400


@pytest.mark.django_db
def test_create_second_primary_fails(api_client, course_certification_mapping, course, db):
    from certification.models import Certification
    cert2 = Certification.objects.create(name='Cert 2', code='CERT-002')
    r = api_client.post(
        URL_LIST,
        {'course': course.pk, 'certification': cert2.pk, 'primary_mapping': True},
        format='json',
    )
    assert r.status_code == 400


@pytest.mark.django_db
def test_filter_by_course_id(api_client, course_certification_mapping, course):
    r = api_client.get(URL_LIST + f'?course_id={course.pk}')
    assert r.json()['data']['count'] == 1


@pytest.mark.django_db
def test_filter_by_certification_id(api_client, course_certification_mapping, certification):
    r = api_client.get(URL_LIST + f'?certification_id={certification.pk}')
    assert r.json()['data']['count'] == 1


@pytest.mark.django_db
def test_retrieve_success(api_client, course_certification_mapping):
    r = api_client.get(detail_url(course_certification_mapping.pk))
    assert r.status_code == 200
    assert r.json()['data']['id'] == course_certification_mapping.pk


@pytest.mark.django_db
def test_retrieve_not_found(api_client):
    r = api_client.get(detail_url(99999))
    assert r.status_code == 404


@pytest.mark.django_db
def test_soft_delete(api_client, course_certification_mapping):
    r = api_client.delete(detail_url(course_certification_mapping.pk))
    assert r.status_code == 204
    course_certification_mapping.refresh_from_db()
    assert course_certification_mapping.is_active is False


@pytest.mark.django_db
def test_patch_primary_false(api_client, course_certification_mapping):
    r = api_client.patch(
        detail_url(course_certification_mapping.pk),
        {'primary_mapping': False},
        format='json',
    )
    assert r.status_code == 200
    assert r.json()['data']['primary_mapping'] is False


@pytest.mark.django_db
def test_invalid_course_id_filter(api_client):
    r = api_client.get(URL_LIST + '?course_id=abc')
    assert r.status_code == 400
