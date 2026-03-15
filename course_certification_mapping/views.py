"""
CourseCertificationMapping views.
"""
import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.mixins import MappingEntityMixin
from core.swagger import (
    mapping_single_response, mapping_list_response,
    mapping_request_schema, MAPPING_LIST_PARAMS, id_filter_param,
)
from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer

logger = logging.getLogger('app')
_TAG = ['Course-Certification Mappings']
_PARENT = 'Course'
_CHILD = 'Certification'


class CourseCertificationMappingListView(MappingEntityMixin, APIView):
    model = CourseCertificationMapping
    serializer_class = CourseCertificationMappingSerializer
    entity_label = 'Course-Certification Mapping'
    parent_id_param = 'course_id'
    child_id_param = 'certification_id'

    @swagger_auto_schema(
        operation_summary='List all Course-Certification Mappings',
        manual_parameters=MAPPING_LIST_PARAMS + [
            id_filter_param(_PARENT), id_filter_param(_CHILD),
        ],
        responses={200: mapping_list_response(_PARENT, _CHILD)},
        tags=_TAG,
    )
    def get(self, request: Request) -> Response:
        return self.list(request)

    @swagger_auto_schema(
        operation_summary='Create a Course-Certification Mapping',
        operation_description=(
            'Links a Course to a Certification.\n\n'
            '**Constraints:**\n'
            '- The (course, certification) pair must be unique.\n'
            '- Only one mapping per Course can have `primary_mapping=True`.'
        ),
        request_body=mapping_request_schema(_PARENT, _CHILD),
        responses={201: mapping_single_response(_PARENT, _CHILD), 400: 'Validation error'},
        tags=_TAG,
    )
    def post(self, request: Request) -> Response:
        return self.create(request)


class CourseCertificationMappingDetailView(MappingEntityMixin, APIView):
    model = CourseCertificationMapping
    serializer_class = CourseCertificationMappingSerializer
    entity_label = 'Course-Certification Mapping'
    parent_id_param = 'course_id'
    child_id_param = 'certification_id'

    @swagger_auto_schema(
        operation_summary='Retrieve a Course-Certification Mapping',
        responses={200: mapping_single_response(_PARENT, _CHILD), 404: 'Not found'},
        tags=_TAG,
    )
    def get(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)

    @swagger_auto_schema(
        operation_summary='Full update a Course-Certification Mapping',
        request_body=mapping_request_schema(_PARENT, _CHILD),
        responses={200: mapping_single_response(_PARENT, _CHILD), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def put(self, request: Request, pk: int) -> Response:
        return self.update(request, pk)

    @swagger_auto_schema(
        operation_summary='Partial update a Course-Certification Mapping',
        request_body=mapping_request_schema(_PARENT, _CHILD),
        responses={200: mapping_single_response(_PARENT, _CHILD), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def patch(self, request: Request, pk: int) -> Response:
        return self.update(request, pk, partial=True)

    @swagger_auto_schema(
        operation_summary='Soft-delete a Course-Certification Mapping',
        responses={204: 'Soft-deleted', 404: 'Not found'},
        tags=_TAG,
    )
    def delete(self, request: Request, pk: int) -> Response:
        return self.destroy(request, pk)
