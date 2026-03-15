"""
Course views — list/create and retrieve/update/delete.
"""
import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.mixins import MasterEntityMixin
from core.swagger import (
    master_single_response, master_list_response,
    master_request_schema, COMMON_LIST_PARAMS, id_filter_param,
)
from product_course_mapping.models import ProductCourseMapping
from .models import Course
from .serializers import CourseSerializer

logger = logging.getLogger('app')
_TAG = ['Courses']


class CourseListView(MasterEntityMixin, APIView):
    model = Course
    serializer_class = CourseSerializer
    entity_label = 'Course'
    child_id_param = 'product_id'
    child_mapping_model = ProductCourseMapping
    child_mapping_field = 'course_id'

    @swagger_auto_schema(
        operation_summary='List all Courses',
        operation_description='Filter by `product_id` to get Courses linked to a specific parent entity.',
        manual_parameters=COMMON_LIST_PARAMS + [id_filter_param('product')],
        responses={200: master_list_response('Course')},
        tags=_TAG,
    )
    def get(self, request: Request) -> Response:
        return self.list(request)

    @swagger_auto_schema(
        operation_summary='Create a Course',
        request_body=master_request_schema('Course'),
        responses={201: master_single_response('Course'), 400: 'Validation error'},
        tags=_TAG,
    )
    def post(self, request: Request) -> Response:
        return self.create(request)


class CourseDetailView(MasterEntityMixin, APIView):
    model = Course
    serializer_class = CourseSerializer
    entity_label = 'Course'

    @swagger_auto_schema(
        operation_summary='Retrieve a Course',
        responses={200: master_single_response('Course'), 404: 'Not found'},
        tags=_TAG,
    )
    def get(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)

    @swagger_auto_schema(
        operation_summary='Full update a Course',
        request_body=master_request_schema('Course'),
        responses={200: master_single_response('Course'), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def put(self, request: Request, pk: int) -> Response:
        return self.update(request, pk)

    @swagger_auto_schema(
        operation_summary='Partial update a Course',
        request_body=master_request_schema('Course'),
        responses={200: master_single_response('Course'), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def patch(self, request: Request, pk: int) -> Response:
        return self.update(request, pk, partial=True)

    @swagger_auto_schema(
        operation_summary='Soft-delete a Course',
        operation_description='Marks the record as inactive. Data is preserved in the database.',
        responses={204: 'Soft-deleted', 404: 'Not found'},
        tags=_TAG,
    )
    def delete(self, request: Request, pk: int) -> Response:
        return self.destroy(request, pk)
