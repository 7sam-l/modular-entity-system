"""
Vendor views — list/create and retrieve/update/delete.
"""
import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.mixins import MasterEntityMixin
from core.swagger import (
    master_single_response, master_list_response,
    master_request_schema, COMMON_LIST_PARAMS,
)
from .models import Vendor
from .serializers import VendorSerializer

logger = logging.getLogger('app')
_TAG = ['Vendors']


class VendorListView(MasterEntityMixin, APIView):
    model = Vendor
    serializer_class = VendorSerializer
    entity_label = 'Vendor'

    @swagger_auto_schema(
        operation_summary='List all Vendors',
        manual_parameters=COMMON_LIST_PARAMS,
        responses={200: master_list_response('Vendor')},
        tags=_TAG,
    )
    def get(self, request: Request) -> Response:
        return self.list(request)

    @swagger_auto_schema(
        operation_summary='Create a Vendor',
        request_body=master_request_schema('Vendor'),
        responses={201: master_single_response('Vendor'), 400: 'Validation error'},
        tags=_TAG,
    )
    def post(self, request: Request) -> Response:
        return self.create(request)


class VendorDetailView(MasterEntityMixin, APIView):
    model = Vendor
    serializer_class = VendorSerializer
    entity_label = 'Vendor'

    @swagger_auto_schema(
        operation_summary='Retrieve a Vendor',
        responses={200: master_single_response('Vendor'), 404: 'Not found'},
        tags=_TAG,
    )
    def get(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)

    @swagger_auto_schema(
        operation_summary='Full update a Vendor',
        request_body=master_request_schema('Vendor'),
        responses={200: master_single_response('Vendor'), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def put(self, request: Request, pk: int) -> Response:
        return self.update(request, pk)

    @swagger_auto_schema(
        operation_summary='Partial update a Vendor',
        request_body=master_request_schema('Vendor'),
        responses={200: master_single_response('Vendor'), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def patch(self, request: Request, pk: int) -> Response:
        return self.update(request, pk, partial=True)

    @swagger_auto_schema(
        operation_summary='Soft-delete a Vendor',
        operation_description='Marks the record as inactive. Data is preserved in the database.',
        responses={204: 'Soft-deleted', 404: 'Not found'},
        tags=_TAG,
    )
    def delete(self, request: Request, pk: int) -> Response:
        return self.destroy(request, pk)
