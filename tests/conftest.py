"""Shared pytest fixtures."""

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def vendor(db):
    from vendor.models import Vendor
    return Vendor.objects.create(name='Acme Corp', code='ACME', description='Test vendor')


@pytest.fixture
def product(db):
    from product.models import Product
    return Product.objects.create(name='Cloud Suite', code='CLOUD-001', description='Test product')


@pytest.fixture
def course(db):
    from course.models import Course
    return Course.objects.create(name='AWS Fundamentals', code='AWS-101', description='Test course')


@pytest.fixture
def certification(db):
    from certification.models import Certification
    return Certification.objects.create(name='AWS Certified', code='AWS-CCP', description='Test cert')


@pytest.fixture
def vendor_product_mapping(db, vendor, product):
    from vendor_product_mapping.models import VendorProductMapping
    return VendorProductMapping.objects.create(vendor=vendor, product=product, primary_mapping=True)


@pytest.fixture
def product_course_mapping(db, product, course):
    from product_course_mapping.models import ProductCourseMapping
    return ProductCourseMapping.objects.create(product=product, course=course, primary_mapping=True)


@pytest.fixture
def course_certification_mapping(db, course, certification):
    from course_certification_mapping.models import CourseCertificationMapping
    return CourseCertificationMapping.objects.create(
        course=course, certification=certification, primary_mapping=True
    )
