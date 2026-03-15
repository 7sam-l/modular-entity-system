"""
Certification views — list/create and retrieve/update/delete.
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
from course_certification_mapping.models import CourseCertificationMapping
from .models import Certification
from .serializers import CertificationSerializer

logger = logging.getLogger('app')
_TAG = ['Certifications']


class CertificationListView(MasterEntityMixin, APIView):
    model = Certification
    serializer_class = CertificationSerializer
    entity_label = 'Certification'
    child_id_param = 'course_id'
    child_mapping_model = CourseCertificationMapping
    child_mapping_field = 'certification_id'

    @swagger_auto_schema(
        operation_summary='List all Certifications',
        operation_description='Filter by `course_id` to get Certifications linked to a specific parent entity.',
        manual_parameters=COMMON_LIST_PARAMS + [id_filter_param('course')],
        responses={200: master_list_response('Certification')},
        tags=_TAG,
    )
    def get(self, request: Request) -> Response:
        return self.list(request)

    @swagger_auto_schema(
        operation_summary='Create a Certification',
        request_body=master_request_schema('Certification'),
        responses={201: master_single_response('Certification'), 400: 'Validation error'},
        tags=_TAG,
    )
    def post(self, request: Request) -> Response:
        return self.create(request)


class CertificationDetailView(MasterEntityMixin, APIView):
    model = Certification
    serializer_class = CertificationSerializer
    entity_label = 'Certification'

    @swagger_auto_schema(
        operation_summary='Retrieve a Certification',
        responses={200: master_single_response('Certification'), 404: 'Not found'},
        tags=_TAG,
    )
    def get(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)

    @swagger_auto_schema(
        operation_summary='Full update a Certification',
        request_body=master_request_schema('Certification'),
        responses={200: master_single_response('Certification'), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def put(self, request: Request, pk: int) -> Response:
        return self.update(request, pk)

    @swagger_auto_schema(
        operation_summary='Partial update a Certification',
        request_body=master_request_schema('Certification'),
        responses={200: master_single_response('Certification'), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def patch(self, request: Request, pk: int) -> Response:
        return self.update(request, pk, partial=True)

    @swagger_auto_schema(
        operation_summary='Soft-delete a Certification',
        operation_description='Marks the record as inactive. Data is preserved in the database.',
        responses={204: 'Soft-deleted', 404: 'Not found'},
        tags=_TAG,
    )
    def delete(self, request: Request, pk: int) -> Response:
        return self.destroy(request, pk)
